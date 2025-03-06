from app.websites.kunnu import KunNu
from app.websites.site import Site
from app.websites.sudugu import SuDuGu

# 域名对应的类
domain_mapping = {
    "www.kunnu.com": KunNu,
    "www.sudugu.com": SuDuGu,
}


def get_site_instance(domain: str) -> Site:
    """
    工厂函数，根据域名返回对应的实例

    Args:
        domain (str): 域名

    Returns:
        Site: 返回对应的实例
    """
    site_class = domain_mapping.get(domain)
    if site_class:
        return site_class()
    else:
        raise ValueError(f"No class found for domain: {domain}")
