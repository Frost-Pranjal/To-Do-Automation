To extract the access token for Graph API, you need to authenticate your app using the Microsoft Identity Platform. Here’s how you can do it step by step:

---

### 1. **Register Your App in Azure AD**
   - Log in to the [Azure portal](https://portal.azure.com/).
   - Go to **Azure Active Directory** > **App registrations** > **New registration**.
   - Fill out the details:
     - **Name:** Your app name.
     - **Supported account types:** Choose as per your requirement (e.g., single-tenant or multi-tenant).
     - **Redirect URI:** Set this if you’re using a web or mobile app.
   - Click **Register**.

---

### 2. **Note Key App Details**
   - **Application (Client) ID:** Found in the app overview.
   - **Directory (Tenant) ID:** Found in the app overview.
   - **Client Secret:** Generate one by navigating to **Certificates & secrets** > **New client secret**. Copy it securely.

---

### 3. **Request Access Token**
Use the following Python code to request an access token. This requires the `requests` library:

# Python: Script for the Acquiring the Access Token

import requests

def get_access_token(tenant_id, client_id, client_secret, scope="https://graph.microsoft.com/.default"):
    """
    Fetch an access token for Microsoft Graph API.

    Args:
        tenant_id (str): Azure AD Tenant ID.
        client_id (str): Application (Client) ID.
        client_secret (str): Application secret.
        scope (str): Scopes for the API, default is Graph API.

    Returns:
        str: Access token.
    """
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": scope,
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Failed to fetch access token: {response.status_code}")
        print(response.json())
        return None


# Example usage:
tenant_id = "YOUR_TENANT_ID"
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

access_token = get_access_token(tenant_id, client_id, client_secret)
if access_token:
    print(f"Access Token: {access_token}")
```

---

### 4. **Use the Access Token**
Once you have the token, include it in the `Authorization` header when making requests to the Graph API:

```python
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
print(response.json())
```

---

### Additional Notes
- **Scope:** Adjust the scope depending on the resources you need access to (e.g., `https://graph.microsoft.com/User.Read`).
- **Token Expiry:** Tokens are typically valid for an hour. Automate the refresh if needed.
- **Interactive Login:** If you want user-based access tokens, you will need to implement OAuth 2.0 authorization code flow. Let me know if you need help with this!