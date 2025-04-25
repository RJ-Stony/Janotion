# 로그인 체크 미들웨어가 있다면 주석 처리

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # 로그인 체크 로직 주석 처리
        # if not request.user.is_authenticated and request.path != '/login/':
        #     return redirect('/login/')
        
        response = self.get_response(request)
        return response
