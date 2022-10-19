

#SET MAX DELAY
MAX_DELAY = 2.5

#PROXIES
proxies = {"user" : {"proxy_port": "sample", "username":"sample", "password": "sample"}
            }


#CSS SELECTORS

num_companies_selector = 'div[class="span7"]>h2'
items_page_selector = 'li[class*="search-result company "] a[class*="company_search_result"]'
jurisdiction_filter_selector = 'div[class="facet jurisdiction_code selected sidebar-item"]>ul li'

#REGULAR EXPRESSION PATTERNS
oc_results_pattern = "\d{1,}\,\d{3,}\.\d{2}|\d{3}\.\d{2}|\d{1,}\,\d{3,}|\d{2,}|\d{2,}\.\d{2}|\d"
west_pattern = '\(Canada\)|United Kingdom|Australia|New Zealand|Ireland|Germany|France|Netherlands|Belgium|Denmark|Finland|Singapore|Sweden|Spain|Japan|Switzerland|Austria|Norway'