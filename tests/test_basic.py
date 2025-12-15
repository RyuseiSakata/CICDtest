from timer_app.app import app

def test_health():
 c=app.test_client(); r=c.get('/health'); assert r.get_json()=={'status':'ok'}
