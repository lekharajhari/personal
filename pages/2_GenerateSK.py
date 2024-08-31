import streamlit as st
import requests

def get_sk_info(secret_key: str) -> dict:
    url = f"https://api.voidex.dev/api/skinfo?sk={secret_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Request failed: {e}")
        return None

def main():
    st.title("Stripe Secret Key Info")
    secret_key = st.text_input("Please enter your Stripe secret key:")

    if secret_key:
        result = get_sk_info(secret_key)

        if result:
            if 'error' in result:
                if result['error'] == 'Failed to fetch account data':
                    st.error({"status": "Invalid key"})
                elif result['error'] == 'Your account cannot currently make live charges.':
                    st.error({
                        "status": "Integration off",
                        "error": result['error'],
                        "country": result.get('country', 'Not available'),
                        "default_currency": result.get('default_currency', 'Not available')
                    })
                else:
                    st.error({"status": "Error", "error": result['error']})
            else:
                if 'available_balance' in result:
                    st.success({
                        "status": "Key is live",
                        "available_balance": result['available_balance'],
                        "country": result.get('country', 'Not available'),
                        "currency": result.get('currency', 'Not available'),
                        "pending_balance": result.get('pending_balance', 'Not available')
                    })
                else:
                    st.error({"status": "Key is not present or available balance is not available."})
        else:
            st.error({"status": "Failed to retrieve information about the secret key."})

if __name__ == "__main__":
    main()