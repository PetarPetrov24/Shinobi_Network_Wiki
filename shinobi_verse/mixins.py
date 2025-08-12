class GreetingMixin:
    def get_greeting_message(self):
        user = self.request.user
        if user.is_authenticated:
            if hasattr(user, 'profile') and user.profile.nickname:
                if user.is_superuser:
                    return f"Welcome, mighty {user.profile.nickname}."
                elif user.is_staff:
                    return f"Greetings, honorable {user.profile.nickname}."
                else:
                    return f"Welcome back, {user.profile.nickname}!"
            else:
                return "You haven’t set a nickname yet."
        return "Hello friendly visitor, here in Shinobi Archives you can see all created shinobi."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['greeting_message'] = self.get_greeting_message()
        return context