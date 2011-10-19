import oauth2 as oauth


def oauth_req(url, key, secret, http_method="GET", post_body=None,
        http_headers=None):
    consumer = oauth.Consumer(key=key, secret=secret)
    token = oauth.Token(key=key, secret=secret)
    client = oauth.Client(consumer, token)
 
    resp, content = client.request(
        url,
        method=http_method,
        body=post_body,
        headers=http_headers
    )
    return content
 
posts_list = oauth_req(
  'http://localhost:8000/api/posts.json',
  'testkey', 'testsecret'
)
