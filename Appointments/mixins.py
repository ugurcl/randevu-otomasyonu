from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

class VerifiedUserMixin(LoginRequiredMixin):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not hasattr(request.user, 'profile') or not request.user.profile.is_verified:
            return redirect('index')
        
        return super().dispatch(request, *args, **kwargs)