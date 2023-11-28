import json

import requests


def get_data(url):
    headers = {
        'authority': 'api.metro-cc.ru',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'origin': 'https://online.metro-cc.ru',
        'referer': 'https://online.metro-cc.ru/',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    info = []
    countries = ["moscow", "saint-petersburg"]

    # Id Московского магазина - 10 / Санкт-Петербурга - 15
    for country_id in [15, 10]:
        json_data = {
            'query': '\n  query Query($storeId: Int!, $slug: String!, $attributes:[AttributeFilter], $filters: [FieldFilter], $from: Int!, $size: Int!, $sort: InCategorySort, $in_stock: Boolean, $eshop_order: Boolean, $is_action: Boolean, $price_levels: Boolean) {\n    category (storeId: $storeId, slug: $slug, inStock: $in_stock, eshopAvailability: $eshop_order, isPromo: $is_action, priceLevels: $price_levels) {\n      id\n      name\n      slug\n      id\n      parent_id\n      meta {\n        description\n        h1\n        title\n        keywords\n      }\n      disclaimer\n      description {\n        top\n        main\n        bottom\n      }\n#      treeBranch {\n#        id\n#        name\n#        slug\n#        children {\n#          category_type\n#          id\n#          name\n#          slug\n#          children {\n#            category_type\n#            id\n#            name\n#            slug\n#            children {\n#              category_type\n#              id\n#              name\n#              slug\n#              children {\n#                category_type\n#                id\n#                name\n#                slug\n#              }\n#            }\n#          }\n#        }\n#      }\n      breadcrumbs {\n        category_type\n        id\n        name\n        parent_id\n        parent_slug\n        slug\n      }\n      promo_banners {\n        id\n        image\n        name\n        category_ids\n        virtual_ids\n        type\n        sort_order\n        url\n        is_target_blank\n        analytics {\n          name\n          category\n          brand\n          type\n          start_date\n          end_date\n        }\n      }\n\n\n      dynamic_categories(from: 0, size: 9999) {\n        slug\n        name\n        id\n        category_type\n      }\n      filters {\n        facets {\n          key\n          total\n          filter {\n            id\n            name\n            display_title\n            is_list\n            is_main\n            text_filter\n            is_range\n            category_id\n            category_name\n            values {\n              slug\n              text\n              total\n            }\n          }\n        }\n      }\n      total\n      prices {\n        max\n        min\n      }\n      pricesFiltered {\n        max\n        min\n      }\n      products(attributeFilters: $attributes, from: $from, size: $size, sort: $sort, fieldFilters: $filters)  {\n        health_warning\n        limited_sale_qty\n        id\n        slug\n        name\n        name_highlight\n        article\n        main_article\n        main_article_slug\n        is_target\n        category_id\n        url\n        images\n        pick_up\n        rating\n        icons {\n          id\n          badge_bg_colors\n          rkn_icon\n          caption\n          image\n          type\n          is_only_for_sales\n          stores\n          caption_settings {\n            colors\n            text\n          }\n          stores\n          sort\n          image_png\n          image_svg\n          description\n          end_date\n          start_date\n          status\n        }\n        manufacturer {\n          id\n          image\n          name\n        }\n        packing {\n          size\n          type\n          pack_factors {\n            instamart\n          }\n        }\n        stocks {\n          value\n          text\n          eshop_availability\n          scale\n          prices_per_unit {\n            old_price\n            offline {\n              price\n              old_price\n              type\n              offline_discount\n              offline_promo\n            }\n            price\n            is_promo\n            levels {\n              count\n              price\n            }\n            online_levels {\n              count\n              price\n              discount\n            }\n            discount\n          }\n          prices {\n            price\n            is_promo\n            old_price\n            offline {\n              old_price\n              price\n              type\n              offline_discount\n              offline_promo\n            }\n            levels {\n              count\n              price\n            }\n            online_levels {\n              count\n              price\n              discount\n            }\n            discount\n          }\n        }\n      }\n    }\n  }\n',
            'variables': {
                'storeId': country_id,
                'sort': 'default',
                'size': 100,
                'from': 0,
                'filters': [
                    {
                        'field': 'main_article',
                        'value': '0',
                    },
                ],
                'attributes': [],
                'in_stock': True,
                'eshop_order': False,
                'allStocks': False,
                'slug': 'rastvorimiy-kofe',
            },
        }

        response = requests.post(url, headers=headers,
                                 json=json_data).json()

        products = response.get("data").get("category").get("products")
        country = countries.pop()
        for product in products:
            price = product.get("stocks")[0]["prices_per_unit"].get("old_price")
            info.append(
                {
                    "id": product.get("article"),
                    "name": product.get("name"),
                    "url": "https://online.metro-cc.ru" + product.get("url"),
                    "old_price": price if price else product.get("stocks")[0]["prices"].get("price"),
                    "new_price": product.get("stocks")[0]["prices"].get("price"),
                    "brand": product.get("manufacturer").get("name"),
                    "country": country
                }
            )

    with open("result.json", "w", encoding="utf-8") as file:
        json.dump(info, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    url_address = "https://api.metro-cc.ru/products-api/graph"
    get_data(url_address)
