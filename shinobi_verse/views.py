from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from shinobi_verse.forms import RegisterForm, LoginForm, ShinobiForm, CommentForm, ClanForm, JutsuForm, ProfileForm
from shinobi_verse.models import Shinobi, Like, Clan, Jutsu, Profile
from shinobi_verse.mixins import GreetingMixin
from .forms import CommentForm

# Create your views here.

class ShinobiListView(ListView):
    model = Shinobi
    template_name = 'Shinobi_CRUD/shinobi_list.html'
    context_object_name = 'shinobi_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(Shinobi)
            liked_shinobi_ids = Like.objects.filter(
                user=self.request.user,
                content_type=content_type,
                object_id__in=context['shinobi_list'].values_list('pk', flat=True)
            ).values_list('object_id', flat=True)
            context['liked_shinobi_ids'] = liked_shinobi_ids
        else:
            context['liked_shinobi_ids'] = []
        return context


class ShinobiDetailView(GreetingMixin, DetailView):
    model = Shinobi
    template_name = 'Shinobi_CRUD/shinobi_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shinobi'] = self.object
        context['comment_form'] = CommentForm()
        return context


class ShinobiCreateView(LoginRequiredMixin, CreateView):
    model = Shinobi
    form_class = ShinobiForm
    template_name = 'Shinobi_CRUD/shinobi_form.html'
    success_url = reverse_lazy('shinobi_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ShinobiUpdateView(LoginRequiredMixin, UpdateView):
    model = Shinobi
    form_class = ShinobiForm
    template_name = 'Shinobi_CRUD/shinobi_form.html'
    success_url = reverse_lazy('shinobi_list')


class ShinobiDeleteView(LoginRequiredMixin, DeleteView):
    model = Shinobi
    template_name = 'Shinobi_CRUD/shinobi_delete.html'
    success_url = reverse_lazy('shinobi_list')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created!')
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid Credentials')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')



@login_required
def like_view(request, model_name, object_id):
    content_type = ContentType.objects.get(model=model_name)
    obj = content_type.model_class().objects.filter(id=object_id)

    try:
        obj = content_type.model_class().objects.get(id=object_id)
    except content_type.model_class().DoesNotExist:
        messages.error(request, "Item not found.")
        return redirect('home')

    like, created = Like.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=object_id)

    if not created:
        like.delete()
        messages.info(request, "You unliked this.")
    else:
        messages.success(request, "You liked this.")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def comment_view(request, model_name, object_id):
    content_type = ContentType.objects.get(model=model_name)
    obj = content_type.get_object_for_this_type(id=object_id)

    try:
        obj = content_type.get_object_for_this_type(id=object_id)
    except content_type.model_class().DoesNotExist:
        messages.error(request, "Item not found.")
        return redirect('home')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = content_type
            comment.object_id = object_id
            comment.save()
            return redirect(request.META.get('HTTP_REFERER', 'home'))
    else:
        form = CommentForm()
    return render(request, 'includes/add_comment.html', {'form': form, 'object': obj})


def home_view(request):
    shinobies = Shinobi.objects.order_by('-created_at')
    clans = Clan.objects.filter()
    jutsus = Jutsu.objects.filter()

    context = {
        'shinobies': shinobies,
        'clans': clans,
        'jutsus': jutsus,
    }
    return render(request, 'home.html', context)


def about_view(request):
    return render(request, 'about.html')

@login_required
def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    shinobies = Shinobi.objects.filter(approved=True)

    return render(request, 'profile.html', {
        'shinobies': shinobies,
        'form': form,
        'profile': profile,
        'user': user
    })


# Clan - CBV

class ClanListView(ListView):
    model = Clan
    template_name = 'Clan_CRUD/clan_list.html'


class ClanDetailView(GreetingMixin, DetailView):
    model = Clan
    template_name = 'Clan_CRUD/clan_detail.html'


class ClanCreateView(CreateView):
    model = Clan
    form_class = ClanForm
    template_name = 'Clan_CRUD/clan_form.html'
    success_url = reverse_lazy('clan_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ClanUpdateView(UpdateView):
    model = Clan
    form_class = ClanForm
    template_name = 'Clan_CRUD/clan_form.html'
    success_url = reverse_lazy('clan_list')


class ClanDeleteView(DeleteView):
    model = Clan
    template_name = 'Clan_CRUD/clan_delete.html'
    success_url = reverse_lazy('clan_list')

# Jutsu - CBV


class JutsuListView(ListView):
    model = Jutsu
    template_name = 'Jutsu_CRUD/jutsu_list.html'


class JutsuDetailView(GreetingMixin, DetailView):
    model = Jutsu
    template_name = 'Jutsu_CRUD/jutsu_detail.html'


class JutsuCreateView(CreateView):
    model = Jutsu
    form_class = JutsuForm
    template_name = 'Jutsu_CRUD/jutsu_form.html'
    success_url = reverse_lazy('jutsu_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class JutsuUpdateView(UpdateView):
    model = Jutsu
    form_class = JutsuForm
    template_name = 'Jutsu_CRUD/jutsu_form.html'
    success_url = reverse_lazy('jutsu_list')


class JutsuDeleteView(DeleteView):
    model = Jutsu
    template_name = 'Jutsu_CRUD/jutsu_delete.html'
    success_url = reverse_lazy('jutsu_list')

