from bs4 import BeautifulSoup
import requests
import lxml.html.clean as clean
import sys


def login_with_saml(sp_login_url, idp_username, idp_password):
    """
    模拟通过SAML协议登录Web应用
    
    Args:
        sp_login_url (str): 服务提供商(SP)的登录入口URL
        idp_username (str): 身份提供商(IdP)的用户名
        idp_password (str): 身份提供商(IdP)的密码
    
    Returns:
        requests.Session: 包含登录后会话的请求对象
    """
    
    # 创建会话对象，保持Cookies
    session = requests.Session()
    
    try:
        # 1. 访问SP登录页面，获取SAMLRequest
        print("Step 1: Accessing SP login page...")
        response = session.get(sp_login_url)
        
        # 解析SAMLRequest，这通常是一个隐藏的表单字段
        soup = BeautifulSoup(response.text, 'html.parser')
        saml_request = soup.find('input', {'name': 'SAMLRequest'})['value']
        idp_sso_url = soup.find('form', {'method': 'post'})['action']
        
        print(f"   Extracted IdP SSO URL: {idp_sso_url}")
        
        # 2. 提交SAMLRequest到IdP的SSO端点
        print("Step 2: Submitting SAMLRequest to IdP...")
        response = session.post(
            idp_sso_url,
            data={
                'SAMLRequest': saml_request,
                'RelayState': ''  # 有时可能为空或包含其他状态信息
            }
        )
        
        # 3. 在IdP的登录页面上提交用户凭证
        # 注意: 实际表单字段名可能不同，需要根据IdP的页面调整
        print("Step 3: Submitting credentials to IdP login page...")
        
        # 解析IdP登录页面，查找登录表单
        login_soup = BeautifulSoup(response.text, 'html.parser')
        login_form = login_soup.find('form')
        login_url = login_form['action'] if login_form and login_form.get('action') else idp_sso_url
        
        # 准备登录数据
        login_data = {}
        for input_tag in login_form.find_all('input'):
            name = input_tag.get('name')
            value = input_tag.get('value', '')
            if name and name not in ['username', 'password']:
                login_data[name] = value
                
        login_data['username'] = idp_username
        login_data['password'] = idp_password
        
        # 提交登录表单
        response = session.post(login_url, data=login_data)
        
        # 4. 处理SAMLResponse，回到SP
        print("Step 4: Processing SAMLResponse from IdP...")
        soup = BeautifulSoup(response.text, 'html.parser')
        saml_response = soup.find('input', {'name': 'SAMLResponse'})['value']
        sp_acs_url = soup.find('form', {'method': 'post'})['action']  # SP的断言消费者服务URL
        
        # 5. 提交SAMLResponse到SP的断言消费者服务(ACS)
        print("Step 5: Submitting SAMLResponse to SP...")
        response = session.post(
            sp_acs_url,
            data={
                'SAMLResponse': saml_response,
                'RelayState': ''
            }
        )
        
        # 6. 验证登录是否成功
        if response.status_code == 200:
            print("✅ Login successful! Session established.")
            # 此时session已包含必要的认证cookies，可以用于访问受保护资源
            return session
        else:
            print(f"❌ Login failed with status code: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ An error occurred during SAML login: {str(e)}")
        return None


def main():
    #SP_LOGIN_URL = "https://login.microsoftonline.com/3bd97919-57c3-48d3-9e9a-8e4c01614a8f/saml2?SAMLRequest=jZJBT%2BMwEIX%2FSuS7EztOm8ZqirqL0CKx2tIGDntznClYSuyuxwmIX79R0gq4II6W38ybN9%2Bsr167NhrAo3G2JDxmJAKrXWPsU0keqhu6IlebNaquTU9y24dnu4d%2FPWCIxkKLcv4pSe%2BtdAoNSqs6QBm0PGx%2F38k0ZvLkXXDatSTaIoIPo9VPZ7HvwB%2FAD0bDw%2F6uJM8hnFAmCZrBIH2BOlZ9cJ0LZgD6omysXZe07snYZHJNEF2i3noPJLoeJzJWhSnFpdGkjTujvUN3DM62xsLURdRNkRe8oItcC5qtGkELKBRdQaYZX%2FJMrY6zCYlunNcwJS%2FJUbU4ut1el2S7v18WNYNsQfOGNTTjdU5rlue0YQUXxVKkKVejFncKx0jwXo3Yw63FoGwoScrSBeWcMl5xIVMhhYiXWfqXRLvz2n4YO%2BP4asf1LEL5q6p2dPfnUJHo8YJ1FJAzRDm5%2B4%2F0vm6sLsjI5luAzmhmrnREP5gGPO0gqEYFNQNbJx%2BH2Zyfnw9s8x8%3D&RelayState=985be197-8e78-4ab9-a1f8-7a9cc186b976"  # SP的SAML登录入口
    SP_LOGIN_URL = "https://sivis-web.automotive-wan.com/"
    IDP_USERNAME = "uidn0076@autmotive-wan.com" 
    IDP_PASSWORD = "patypaty1!"
    
    # 执行SAML登录
    authenticated_session = login_with_saml(SP_LOGIN_URL, IDP_USERNAME, IDP_PASSWORD)
    
    if authenticated_session:
        # 使用获取到的会话访问受保护资源
        #protected_resource_url = "https://sivis-web.automotive-wan.com/"
        protected_resource_url = "https://login.microsoftonline.com/3bd97919-57c3-48d3-9e9a-8e4c01614a8f/saml2"
        response = authenticated_session.get(protected_resource_url)
        
        if response.status_code == 200:
            print("✅ Successfully accessed protected resource")
            # 处理获取到的受保护内容
            # print(response.text)
        else:
            print(f"❌ Failed to access protected resource: {response.status_code}")  

if __name__ == "__main__":
    main()