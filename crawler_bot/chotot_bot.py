import copy
from time import sleep

from crawler_bot.bot import Bot


class ChoTotBot(Bot):
    def parse_ata(self, soup_of_page):
        contents = soup_of_page.find_all("div", {"class": "pr-container"})
        list_clear_data = []
        for content in contents:
            bds_data = {}
            for key, val in self.config_parser.items():
                val_copy = copy.deepcopy(val)
                value = val_copy.pop("value")
                item_val = content.find(**val_copy)
                item_text = None
                if bool(value) and isinstance(value, str):
                    item_text = getattr(item_val, value, None)
                elif bool(value) and isinstance(value, list):
                    item_obj = getattr(item_val, value[0], {})
                    item_text = item_obj.get(value[1], None)
                if bool(item_text):
                    bds_data[key] = item_text.strip()
                else:
                    bds_data[key] = None
            list_clear_data.append(bds_data)
        return list_clear_data

    def auto_craw(self, config):
        type_page = config["type_page"]
        page_from = int(config.get("page_from", 0))
        page_prefix = config.get("page_prefix", 'p')
        page_to = int(config.get("page_to", 1))
        res_all_page = []
        for page in range(page_from, page_to):
            print(f'Start crawler page: {page} ....')
            url_craw = f"{self.base_url}/{type_page}/{page_prefix}{page}"
            result_page = self.crawling(url_craw)
            print(f'Result crawler page: {page} => {len(result_page)}')
            res_all_page.extend(result_page)
            sleep(1)
            if len(res_all_page) > 100:
                self.to_mongo(res_all_page)
                res_all_page = []
        # self.to_csv(res_all_page)
