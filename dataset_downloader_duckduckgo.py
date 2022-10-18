from duckduckgo_search import ddg_images
import requests
import os

class DatasetDownloader:
    def __init__(self, dataset_name, label_data, allowed_extensions):
        """
            # label_data - list of pairs of (label, search word for label)
        """
        self.dataset_name = dataset_name
        self.label_data = label_data
        self.allowed_extensions = allowed_extensions

        # prepare dataset folder
        self.create_dir_if_not_exists(self.dataset_name)

    def download_images(self, search_limit_per_class=1):

        for label_name, search_keyword in self.label_data:
            print("prepare label: '{}'".format(label_name))

            # prepare subdir for label images
            label_subdir = os.path.join(self.dataset_name, label_name)
            self.create_dir_if_not_exists(label_subdir)

            # find images
            image_urls = self.get_image_urls(search_keyword, search_limit_per_class)
            print("found {} images for '{}'".format(len(image_urls), search_keyword))

            # save images
            # print results every 10%
            logging_step = int(0.1 * len(image_urls))
            logging_step = 1 if logging_step == 0 else logging_step

            for n, image_url in enumerate(image_urls):
                extension_pos = image_url.rfind('.')
                if -1 == extension_pos:
                    continue
                image_path = os.path.join(label_subdir, str(n) + image_url[extension_pos:])

                image_bytes = self.download_url_image_bytes(image_url)
                if image_bytes is None:
                    #print('no image bytes')
                    continue

                self.save_image_bytes(image_bytes, image_path)

                if n % logging_step == 0:
                    percent_done = n / len(image_urls) * 100.
                    print("processed {} for {:.1f}%".format(label_name, percent_done))

        print("dataset downloading done.")


    def create_dir_if_not_exists(self, dir_name):
        if not os.path.isdir(dir_name):
            print('create dir:', dir_name)
            os.mkdir(dir_name)

    def get_image_urls(self, keywords, maxnum):
        search_result_data = ddg_images(keywords, region='wt-wt', safesearch='Moderate',
                        size='Medium',# license_image='Public',
                        max_results=maxnum, download=False)

        image_urls = [
            data['image'] for data in search_result_data
            # check file extension
            if any(data['image'].endswith(ext) for ext in self.allowed_extensions)
        ]
        return image_urls

    def download_url_image_bytes(self, image_url):
        try:
            response = requests.get(image_url, timeout=(1.5, 5.5))# 1.5 sec - connect, 5.5 sec - read
        except (requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectionError):
            print('timeout for URL:', image_url)
            return

        if not response.ok:
            print('file cannot be downloaded:', image_url)
            return

        # get content
        image_data = response.content

        return image_data

    def save_image_bytes(self, image_bytes, image_savepath):
        with open(image_savepath, 'wb') as image_file:
            image_file.write(image_bytes)
