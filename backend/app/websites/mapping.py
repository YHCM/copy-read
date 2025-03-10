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
        raise ValueError(f"no class found for domain: {domain}")


def get_site_instances() -> list[Site]:
    """
    获取所有启用域名的实例对象列表

    Returns:
        list[Site]: 所有启用域名的对象列表
    """
    enable_domain = ["www.kunnu.com", "www.sudugu.com"]

    return [get_site_instance(domain) for domain in enable_domain]
