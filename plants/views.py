from django.urls import reverse_lazy, reverse
from django.views import generic
from .forms import PlantForm
from .models import Plant
from django import forms


class PlantSearchForm(forms.Form):
    category = forms.fields.ChoiceField(
        label = 'カテゴリー',
        choices = (
            ('rose', 'バラ'),
            ('decorativeplant', '観葉植物'),
            ('orchid', 'ラン'),
            ('fruittree', '果樹'),
            ('vegetable', '野菜'),
            ('others', 'その他'),
        ),
        required = False,
        widget = forms.widgets.Select
    )

    per_page = forms.fields.ChoiceField(
        label = '表示件数',
        choices = (
        #    (None, "-"),
            (1, "1"),
            (2, "2"),
            (10, "10"),
            (50, "50",),
        ),
        required = False,
        widget = forms.widgets.Select
    )

    def __init__(self, *args, **kwargs):
        super(PlantSearchForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class plant_imagelist(generic.ListView):
    """画像の一覧"""
    model = Plant
    context_object_name = 'plantImages'
    #オブジェクトのサブセットを表示する
    queryset = Plant.objects.order_by('-uetuke_date').prefetch_related(
        'categories',
    )
    #ページネーション
    paginate_by = 2
    page_kwarg = 'page'
    paginate_root_url = reverse_lazy('plants:plant_imagelist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #ログインしていたらplantに編集用のURLを付与する
        if self.request.user.is_authenticated:
            plantimages = context['plantImages']
            for plantimage in plantimages:
                plantimage.edit_url = reverse(f'admin:{plantimage._meta.app_label}_{plantimage._meta.model_name}_change', args=[plantimage.pk])
            context['plantImages'] = plantimages
        
        #検索条件やper_pageを含んだページネーション用URL
        self.paginate_root_url += '?'
        query_dict = self.request.GET.copy()
        if self.page_kwarg in query_dict.keys():
            query_dict.pop(self.page_kwarg)
        for key, value in query_dict.items():
            self.paginate_root_url += f'&{key}={value}'
        context['paginate_root_url'] = self.paginate_root_url

        # 検索フォーム
        context['search_form'] = PlantSearchForm(self.request.GET)
        return context

    def get_queryset(self, **kwargs):
        # 動的なフィルタリング
        queryset = super().get_queryset(**kwargs)
        if self.request.GET.get('category'):
            queryset = queryset.filter(
                categories__slug = self.request.GET.get('category')
            )          
        return queryset

    def get_paginate_by(self, queryset):
        # per_pageをクエリによって動的に変える
        paginate_by = super().get_paginate_by(queryset)
        if self.request.GET.get('per_page'):
            paginate_by = int(self.request.GET.get('per_page'))
        return paginate_by    


class image_add(generic.CreateView):
    """画像の追加"""
    model = Plant
    form_class = PlantForm
    success_url = reverse_lazy('plants:plant_imagelist')


class image_update(generic.UpdateView):
    """画像の更新"""
    model = Plant
    form_class = PlantForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('plants:plant_imagelist')
    
    
class image_delete(generic.DeleteView):
    template_name = 'plants/plant_confirm_delete.html'
    model = Plant
    success_url = reverse_lazy('plants:plant_imagelist')


class index(generic.TemplateView):
    template_name = 'plants/index.html'
    