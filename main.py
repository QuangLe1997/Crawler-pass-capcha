from crawler_bot.batdongsan_bot import BDS_bot

if __name__ == '__main__':
    bat_dong_san_url = "https://batdongsan.com.vn/"
    config = {
        "type_page": "nha-dat-ban",
        "page_from": 0,
        "page_to": 1000
    }
    config_parser = {
        "title": {"name": "span", "class_": "pr-title", "value": "text"},
        "price": {"name": "span", "class_": "price", "value": "text"},
        "area": {"name": "span", "class_": "area", "value": "text"},
        "bedroom": {"name": "span", "class_": "bedroom", "value": "text"},
        "toilet": {"name": "span", "class_": "toilet", "value": "text"},
        "location": {"name": "span", "class_": "location", "value": "text"},
        "product_content": {"name": "div", "class_": "product-content", "value": "text"},
        "time_post": {"name": "span", "class_": "tooltip-time", "value": "text"},
        "contact_name": {"name": "span", "class_": "contact-name", "value": "text"},
        "phone": {"name": "span", "class_": "hidden-phone", "raw": True, "value": ["attrs", "raw"]},
        "url": {"name": "a", "href": True, "value": ["attrs", "href"]}
    }
    bds_bot = BDS_bot('chromedriver.exe', 'batdongsan_data.xlsx', bat_dong_san_url, config_parser)
    bds_bot.auto_craw(config)
