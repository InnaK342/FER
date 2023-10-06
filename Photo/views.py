from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import *
from django.core.files.base import ContentFile


from tensorflow.keras.models import model_from_json
import cv2
import os
import numpy as np
import json


def index(request):
    context = {}
    return render(request, 'Photo/index.html', context)


def photo_form(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = Photo.objects.create(
                photo=request.FILES['photo'],
                author=request.user
            )
            results = predict(photo.photo.url, photo)
            return render(request, 'Photo/photo_form.html', {'photo': photo, 'results': results, 'form': form})
    else:
        form = PhotoForm()
    context = {'form': form}
    return render(request, 'Photo/photo_form.html', context)


def softmax(z): return np.exp(z)/((np.exp(z)).sum())


def predict(photo, photo_object):
    json_file = open('Photo/add_data/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights("Photo/add_data/model_weights.h5")
    face_haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    emotions = ('Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral')
    url = os.path.realpath(os.path.dirname(__file__))[:-6] + photo
    c_img = cv2.imread(url)
    gray_img = cv2.cvtColor(c_img, cv2.COLOR_BGR2GRAY)
    faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.1, 5)
    results = []
    count = 1
    for (x, y, w, h) in faces_detected:
        cv2.rectangle(c_img, (x, y), (x + w, y + h), (0, 0, 0), thickness=2)
        roi_gray = gray_img[y:y + w, x:x + h]
        roi_gray = cv2.resize(roi_gray, (48, 48))

        img = roi_gray.reshape((1, 48, 48, 1))
        img = img / 255.0
        predictions = model.predict(img.reshape((1, 48, 48, 1)))
        results.append({emotions[i]: round(predictions[0][i] * 100, 2) for i in range(len(emotions))})
        max_index = np.argmax(predictions, axis=-1)[0]
        predicted_emotion = emotions[max_index]
        cv2.putText(c_img, predicted_emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(c_img, str(count), (int(x - 30), int(y + h)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        count += 1
    photo_object.result_photo.save('result.jpg', ContentFile(cv2.imencode('.jpg', c_img)[1]))
    results_str = json.dumps(results)
    print(results_str)
    file_results = ContentFile(results_str.encode())
    photo_object.file_results.save('result.txt', file_results)
    return results


class RegisterUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'Photo/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Реєстрація'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'Photo/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизація'
        return context

    def get_success_url(self):
        return reverse_lazy('index')


def logout_user(request):
    logout(request)
    return redirect('login')


def person_page(request, user_id):
    photos = Photo.objects.filter(author=user_id).order_by('-date_added')
    return render(request, 'Photo/person_page.html', {'photos': photos})


def delete_photo(request, photo_id):
    photo = Photo.objects.get(pk=photo_id)
    photo.delete()
    return redirect('person_page', user_id=request.user.pk)




