from dataset_downloader_duckduckgo import *

if __name__ == '__main__':
    dataset_downloader = DatasetDownloader(dataset_name='bears_dataset',
        label_data=[
            ('black', 'black bear'),
            ('grizzly', 'grizzly bear'),
            ('teddy', 'teddy bear')],
        allowed_extensions=['.jpg', '.png', '.jpeg'])
    dataset_downloader.download_images(search_limit_per_class=100)
