from adminboundarymanager.models import AdminBoundarySettings
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.urls import path, reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail_adminsortable.admin import SortableAdminMixin
from wagtail_modeladmin.helpers import AdminURLHelper
from wagtail_modeladmin.options import ModelAdminGroup, ModelAdmin, modeladmin_register
from wagtail_modeladmin.views import CreateView, EditView, IndexView

from .helpers import (DatasetButtonHelper, CategoryButtonHelper, FileLayerButtonHelper)
from .models import (
    SubCategory, GeomanagerSettings,
    Category,
    Dataset,
    Metadata,
    RasterFileLayer,
    MBTSource, WmsLayer, RasterStyle, LayerRasterFile,
    VectorFileLayer, PgVectorTable, RasterTileLayer, VectorTileLayer
)
from .views import (
    upload_raster_file,
    publish_raster,
    delete_raster_upload,
    preview_raster_layers,
    upload_vector_file,
    publish_vector,
    delete_vector_upload,
    preview_vector_layers,
    preview_wms_layers,
    load_stations,
    preview_stations
)
from .views.raster_tile import preview_raster_tile_layers
from .views.vector_tile import preview_vector_tile_layers


@hooks.register('register_admin_urls')
def urlconf_geomanager():
    return [
        path('upload-rasters/', upload_raster_file, name='geomanager_upload_rasters'),
        path('upload-rasters/<uuid:dataset_id>/', upload_raster_file, name='geomanager_dataset_upload_raster'),
        path('upload-rasters/<uuid:dataset_id>/<uuid:layer_id>/', upload_raster_file,
             name='geomanager_dataset_layer_upload_raster'),

        path('publish-rasters/<int:upload_id>/', publish_raster, name='geomanager_publish_raster'),
        path('delete-raster-upload/<int:upload_id>/', delete_raster_upload, name='geomanager_delete_raster_upload'),

        path('preview-raster-layers/<uuid:dataset_id>/', preview_raster_layers,
             name='geomanager_preview_raster_dataset'),
        path('preview-raster-layers/<uuid:dataset_id>/<uuid:layer_id>/', preview_raster_layers,
             name='geomanager_preview_raster_layer'),
        path('upload-vector/', upload_vector_file, name='geomanager_upload_vector'),
        path('upload-vector/<uuid:dataset_id>/', upload_vector_file, name='geomanager_dataset_upload_vector'),
        path('upload-vector/<uuid:dataset_id>/<uuid:layer_id>/', upload_vector_file,
             name='geomanager_dataset_layer_upload_vector'),

        path('publish-vector/<int:upload_id>/', publish_vector, name='geomanager_publish_vector'),
        path('delete-vector-upload/<int:upload_id>/', delete_vector_upload, name='geomanager_delete_vector_upload'),

        path('preview-vector-layers/<uuid:dataset_id>/', preview_vector_layers,
             name='geomanager_preview_vector_dataset'),
        path('preview-vector-layers/<uuid:dataset_id>/<uuid:layer_id>/', preview_vector_layers,
             name='geomanager_preview_vector_layer'),

        path('preview-wms-layers/<uuid:dataset_id>/', preview_wms_layers,
             name='geomanager_preview_wms_dataset'),
        path('preview-wms-layers/<uuid:dataset_id>/<uuid:layer_id>/', preview_wms_layers,
             name='geomanager_preview_wms_layer'),

        path('preview-vector-tile-layers/<uuid:dataset_id>/', preview_vector_tile_layers,
             name='geomanager_preview_vector_tile_dataset'),
        path('preview-vector-tile-layers/<uuid:dataset_id>/<uuid:layer_id>/', preview_vector_tile_layers,
             name='geomanager_preview_vector_tile_layer'),

        path('preview-raster-tile-layers/<uuid:dataset_id>/', preview_raster_tile_layers,
             name='geomanager_preview_raster_tile_dataset'),
        path('preview-raster-tile-layers/<uuid:dataset_id>/<uuid:layer_id>/', preview_raster_tile_layers,
             name='geomanager_preview_raster_tile_layer'),

        path('load-stations/', load_stations, name='geomanager_load_stations'),
        path('preview-stations/', preview_stations, name='geomanager_preview_stations'),
    ]


class ModelAdminCanHide(ModelAdmin):
    hidden = False


class CategoryModelAdmin(SortableAdminMixin, ModelAdminCanHide):
    model = Category
    menu_label = _("Data Categories")
    exclude_from_explorer = True
    button_helper_class = CategoryButtonHelper
    menu_icon = "layer-group"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.list_display = (list(self.list_display) or []) + ["create_dataset", 'view_datasets', ]
        self.create_dataset.__func__.short_description = _('Create Dataset')
        self.view_datasets.__func__.short_description = _('View Datasets')

    def create_dataset(self, obj):
        label = _("Create Dataset")
        button_html = f"""
            <a href="{obj.dataset_create_url()}" class="button button-small button--icon bicolor">
                <span class="icon-wrapper">
                    <svg class="icon icon-plus icon" aria-hidden="true">
                        <use href="#icon-plus"></use>
                    </svg>
                </span>
              {label}
            </a>
        """
        return mark_safe(button_html)

    def view_datasets(self, obj):
        label = _("View Datasets")
        button_html = f"""
            <a href="{obj.datasets_list_url()}" class="button button-small button--icon bicolor button-secondary">
                <span class="icon-wrapper">
                    <svg class="icon icon-list-ul icon" aria-hidden="true">
                        <use href="#icon-list-ul"></use>
                    </svg>
                </span>
                {label}
            </a>
        """
        return mark_safe(button_html)


class DatasetIndexView(IndexView):
    def get_context_data(self, **kwargs):
        context_data = super(DatasetIndexView, self).get_context_data(**kwargs)

        categories_admin_helper = AdminURLHelper(Category)
        url = categories_admin_helper.get_action_url("index")

        context_data.update({
            "custom_create_url": {
                "label": _("Create from categories"),
                "url": url
            }
        })

        return context_data


class DatasetCreateView(CreateView):
    def get_form(self):
        form = super().get_form()
        category_id = self.request.GET.get("category_id")
        if category_id:
            # form.fields["category"].widget.attrs.update({"disabled": "true"})
            form.fields["sub_category"].queryset = SubCategory.objects.filter(category=category_id)
            initial = {**form.initial}
            initial.update({"category": category_id})
            form.initial = initial
        return form


class DatasetModelAdmin(ModelAdminCanHide):
    model = Dataset
    exclude_from_explorer = True
    button_helper_class = DatasetButtonHelper
    list_display = ("__str__", "layer_type",)
    list_filter = ("category", "id",)
    index_template_name = "modeladmin/index_without_custom_create.html"
    menu_icon = "database"

    index_view_class = DatasetIndexView
    create_view_class = DatasetCreateView

    def __init__(self, parent=None):
        super().__init__(parent)
        self.list_display = (list(self.list_display) or []) + ['category_link', 'view_layers', 'upload_files']
        self.category_link.__func__.short_description = _('Category')
        self.view_layers.__func__.short_description = _('View Layers')
        self.upload_files.__func__.short_description = _('Upload Files')

    def category_link(self, obj):
        label = _("Edit Category")
        button_html = f"""
            <a href="{obj.category_url}">
                {label}
            </a>
        """
        return mark_safe(button_html)

    def view_layers(self, obj):
        label = _("Layers")
        button_html = f"""
            <a href="{obj.layers_list_url()}" class="button button-small button--icon bicolor button-secondary">
                <span class="icon-wrapper">
                    <svg class="icon icon-list-ol icon" aria-hidden="true">
                        <use href="#icon-list-ol"></use>
                    </svg>
                </span>
                {label}
            </a>
        """
        return mark_safe(button_html)

    def preview_dataset(self, obj):
        if not obj.preview_url:
            return None

        if obj.layer_type == "vector_file":
            return None

        disabled = "" if obj.can_preview() else "disabled"
        label = _("Preview Dataset")
        button_html = f"""
            <a href="{obj.preview_url}" class="button button-small button--icon button-secondary {disabled}">
                <span class="icon-wrapper">
                    <svg class="icon icon-plus icon" aria-hidden="true">
                        <use href="#icon-view"></use>
                    </svg>
                </span>
                {label}
            </a>
        """
        return mark_safe(button_html)

    def upload_files(self, obj):
        if not obj.upload_url:
            return None

        disabled = "" if obj.has_layers() else "disabled"
        label = _("Upload Files")
        button_html = f"""
            <a href="{obj.upload_url}" class="button button-small bicolor button--icon {disabled}">
                <span class="icon-wrapper">
                    <svg class="icon icon-plus icon" aria-hidden="true">
                        <use href="#icon-upload"></use>
                    </svg>
                </span>
                {label}
            </a>
        """
        return mark_safe(button_html)


class LayerIndexView(IndexView):
    def get_context_data(self, **kwargs):
        context_data = super(LayerIndexView, self).get_context_data(**kwargs)

        dataset_admin_helper = AdminURLHelper(Dataset)
        url = dataset_admin_helper.get_action_url("index")

        context_data.update({
            "custom_create_url": {
                "label": _("Create from datasets"),
                "url": url
            }
        })

        return context_data


class RasterFileLayerCreateView(CreateView):
    def get_form(self):
        form = super().get_form()
        form.fields["dataset"].queryset = Dataset.objects.filter(layer_type="raster_file")

        dataset_id = self.request.GET.get("dataset_id")
        if dataset_id:
            initial = {**form.initial}
            initial.update({"dataset": dataset_id})
            form.initial = initial
        return form


class RasterFileLayerEditView(EditView):
    def get_form(self):
        form = super().get_form()
        form.fields["dataset"].queryset = Dataset.objects.filter(layer_type="raster_file")
        return form


class RasterFileLayerModelAdmin(ModelAdminCanHide):
    model = RasterFileLayer
    hidden = True
    exclude_from_explorer = True
    menu_label = _("File Layers")
    button_helper_class = FileLayerButtonHelper
    index_view_class = LayerIndexView
    create_view_class = RasterFileLayerCreateView
    edit_view_class = RasterFileLayerEditView
    list_display = ("title",)
    list_filter = ("dataset",)
    index_template_name = "modeladmin/index_without_custom_create.html"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.list_display = (list(self.list_display) or []) + ["dataset_link", "upload_files", "uploaded_files",
                                                               "preview_layer"]
        self.dataset_link.__func__.short_description = _("Dataset")
        self.uploaded_files.__func__.short_description = _("Uploaded Files")
        self.upload_files.__func__.short_description = _("Upload Raster Files")
        self.preview_layer.__func__.short_description = _("Preview on Map")

    def dataset_link(self, obj):
        button_html = f"""
        <a href="{obj.dataset.dataset_url()}">
        {obj.dataset.title}
        </a>
        """
        return mark_safe(button_html)

    def upload_files(self, obj):
        label = _("Upload Files")
        button_html = f"""
            <a href="{obj.upload_url}" class="button button-small bicolor button--icon">
                <span class="icon-wrapper">
                    <svg class="icon icon-plus icon" aria-hidden="true">
                        <use href="#icon-upload"></use>
                    </svg>
                </span>
                {label}
            </a>
        """
        return mark_safe(button_html)

    def uploaded_files(self, obj):
        label = _("View Uploaded Files")
        button_html = f"""
            <a href="{obj.get_uploads_list_url()}" class="button button-small button--icon bicolor button-secondary">
                <span class="icon-wrapper">
                    <svg class="icon icon-list-ol icon" aria-hidden="true">
                        <use href="#icon-list-ol"></use>
                    </svg>
                </span>
                {label}
            </a>
        """
        return mark_safe(button_html)

    def preview_layer(self, obj):
        label = _("Preview Layer")
        button_html = f"""
            <a href="{obj.preview_url}" class="button button-small button--icon button-secondary">
                <span class="icon-wrapper">
                    <svg class="icon icon-plus icon" aria-hidden="true">
                        <use href="#icon-view"></use>
                    </svg>
                </span>
                {label}
            </a>
        """
        return mark_safe(button_html)


class MetadataModelAdmin(ModelAdminCanHide):
    model = Metadata
    exclude_from_explorer = True
    menu_icon = 'info-circle'


class ModelAdminGroupWithHiddenItems(ModelAdminGroup):
    def get_submenu_items(self):
        menu_items = []
        item_order = 1
        for model_admin in self.modeladmin_instances:
            if not model_admin.hidden:
                menu_items.append(model_admin.get_menu_item(order=item_order))
                item_order += 1
        return menu_items


class RasterStyleCreateView(CreateView):
    def get_form(self):
        form = super().get_form()

        layer_id = self.request.GET.get("layer_id")

        # add hidden layer_id field to form. We will use it later to update the layer style
        if layer_id:
            try:
                layer = RasterFileLayer.objects.get(pk=layer_id)
                form.fields["layer_id"] = forms.CharField(required=False, widget=forms.HiddenInput())
                form.initial.update({"layer_id": layer.pk})
            except ObjectDoesNotExist:
                pass

        return form

    def form_valid(self, form):
        response = super().form_valid(form)

        # check if we have layer_id in data
        layer_id = form.data.get("layer_id")

        if layer_id:
            try:
                # assign this layer the just created style
                layer = RasterFileLayer.objects.get(pk=layer_id)
                layer.style = self.instance
                layer.save()
            except ObjectDoesNotExist:
                pass

        return response


class RasterStyleModelAdmin(ModelAdminCanHide):
    model = RasterStyle
    exclude_from_explorer = True
    create_view_class = RasterStyleCreateView
    list_display = ("__str__", "min", "max")
    form_view_extra_js = ["geomanager/js/raster_style_extra.js"]
    menu_icon = "palette"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.list_display = (list(self.list_display) or []) + ["preview"]
        self.preview.__func__.short_description = _("Color Preview")

    def preview(self, obj):
        if obj.use_custom_colors:
            return None
        color_list = [f"<li style='background-color:{color};height:20px;flex:1;'><li/>" for color in
                      obj.palette.split(",")]
        html = f"""
            <ul style='display:flex;width:200px;box-shadow: 0 1px 6px rgba(0, 0, 0, 0.12), 0 1px 4px rgba(0, 0, 0, 0.12);'>
                {''.join(color_list)}
            </ul>
        """
        return mark_safe(html)


class WmsLayerCreateView(CreateView):
    def get_form(self):
        form = super().get_form()
        form.fields["dataset"].queryset = Dataset.objects.filter(layer_type="wms")

        dataset_id = self.request.GET.get("dataset_id")
        if dataset_id:
            initial = {**form.initial}
            initial.update({"dataset": dataset_id})
            form.initial = initial
        return form


class WmsLayerModelAdmin(ModelAdminCanHide):
    model = WmsLayer
    exclude_from_explorer = True
    create_view_class = WmsLayerCreateView
    hidden = True
    index_template_name = "modeladmin/index_without_custom_create.html"
    index_view_class = LayerIndexView

    def __init__(self, parent=None):
        super().__init__(parent)
        self.list_display = (list(self.list_display) or []) + ['dataset_link', 'preview_layer']
        self.dataset_link.__func__.short_description = _('Dataset')
        self.preview_layer.__func__.short_description = _('Preview on Map')

    def dataset_link(self, obj):
        button_html = f"""
            <a href="{obj.dataset.dataset_url()}">
                {obj.dataset.title}
            </a>
        """
        return mark_safe(button_html)

    def preview_layer(self, obj):
        label = _("Preview Layer")
        button_html = f"""
            <a href="{obj.preview_url}" class="button button-small button--icon button-secondary">
                <span class="icon-wrapper">
                    <svg class="icon icon-plus icon" aria-hidden="true">
                        <use href="#icon-view"></use>
                    </svg>
                </span>
                {label}
            </a>
        """
        return mark_safe(button_html)


class RasterTileLayerCreateView(CreateView):
    def get_form(self):
        form = super().get_form()
        form.fields["dataset"].queryset = Dataset.objects.filter(layer_type="raster_tile")

        dataset_id = self.request.GET.get("dataset_id")
        if dataset_id:
            initial = {**form.initial}
            initial.update({"dataset": dataset_id})
            form.initial = initial
        return form


class RasterTileLayerModelAdmin(ModelAdminCanHide):
    model = RasterTileLayer
    exclude_from_explorer = True
    create_view_class = RasterTileLayerCreateView
    hidden = True
    index_template_name = "modeladmin/index_without_custom_create.html"
    index_view_class = LayerIndexView
    form_view_extra_js = ["geomanager/js/raster_tile_layer_form.js"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.list_display = (list(self.list_display) or []) + ['dataset_link', 'preview_layer']
        self.dataset_link.__func__.short_description = _('Dataset')
        self.preview_layer.__func__.short_description = _('Preview on Map')

    def dataset_link(self, obj):
        button_html = f"""
            <a href="{obj.dataset.dataset_url()}">
                {obj.dataset.title}
            </a>
        """
        return mark_safe(button_html)

    def preview_layer(self, obj):
        label = _("Preview Layer")
        button_html = f"""
            <a href="{obj.preview_url}" class="button button-small button--icon button-secondary">
                <span class="icon-wrapper">
                    <svg class="icon icon-plus icon" aria-hidden="true">
                        <use href="#icon-view"></use>
                    </svg>
                </span>
                {label}
            </a>
        """
        return mark_safe(button_html)


class VectorTileLayerCreateView(CreateView):
    def get_form(self):
        form = super().get_form()
        form.fields["dataset"].queryset = Dataset.objects.filter(layer_type="vector_tile")

        dataset_id = self.request.GET.get("dataset_id")
        if dataset_id:
            initial = {**form.initial}
            initial.update({"dataset": dataset_id})
            form.initial = initial
        return form


class VectorTileLayerModelAdmin(ModelAdminCanHide):
    model = VectorTileLayer
    exclude_from_explorer = True
    create_view_class = VectorTileLayerCreateView
    hidden = True
    index_template_name = "modeladmin/index_without_custom_create.html"
    index_view_class = LayerIndexView

    def __init__(self, parent=None):
        super().__init__(parent)
        self.list_display = (list(self.list_display) or []) + ['dataset_link', 'preview_layer']
        self.dataset_link.__func__.short_description = _('Dataset')
        self.preview_layer.__func__.short_description = _('Preview on Map')

    def dataset_link(self, obj):
        button_html = f"""
            <a href="{obj.dataset.dataset_url()}">
                {obj.dataset.title}
            </a>
        """
        return mark_safe(button_html)

    def preview_layer(self, obj):
        label = _("Preview Layer")
        button_html = f"""
            <a href="{obj.preview_url}" class="button button-small button--icon button-secondary">
                <span class="icon-wrapper">
                    <svg class="icon icon-plus icon" aria-hidden="true">
                        <use href="#icon-view"></use>
                    </svg>
                </span>
                {label}
            </a>
        """
        return mark_safe(button_html)


class VectorFileLayerCreateView(CreateView):
    def get_form(self):
        form = super().get_form()
        form.fields["dataset"].queryset = Dataset.objects.filter(layer_type="vector_file")

        dataset_id = self.request.GET.get("dataset_id")
        if dataset_id:
            initial = {**form.initial}
            initial.update({"dataset": dataset_id})
            form.initial = initial
        return form


class VectorFileLayerEditView(EditView):
    def get_form(self):
        form = super().get_form()
        form.fields["dataset"].queryset = Dataset.objects.filter(layer_type="vector_file")
        return form


class VectorFileLayerModelAdmin(ModelAdminCanHide):
    model = VectorFileLayer
    hidden = True
    exclude_from_explorer = True
    menu_label = _("Vector Layers")
    index_view_class = LayerIndexView
    create_view_class = VectorFileLayerCreateView
    edit_view_class = VectorFileLayerEditView
    list_display = ("title",)
    list_filter = ("dataset",)
    index_template_name = "modeladmin/index_without_custom_create.html"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.list_display = (list(self.list_display) or []) + ['dataset_link', "uploaded_files", "upload_files",
                                                               'preview_layer']
        self.dataset_link.__func__.short_description = _('Dataset')
        self.uploaded_files.__func__.short_description = _("View Uploaded Files")
        self.upload_files.__func__.short_description = _('Upload Vector Files')
        self.preview_layer.__func__.short_description = _('Preview on Map')

    def dataset_link(self, obj):
        button_html = f"""
            <a href="{obj.dataset.dataset_url()}">
            {obj.dataset.title}
            </a>
        """
        return mark_safe(button_html)

    def upload_files(self, obj):
        disabled = "" if not obj.has_data_table else "disabled"

        label = _("Upload Files")
        button_html = f"""
            <a href="{obj.upload_url}" class="button button-small bicolor button--icon" {disabled}>
                <span class="icon-wrapper">
                    <svg class="icon icon-plus icon" aria-hidden="true">
                        <use href="#icon-upload"></use>
                    </svg>
                </span>
                {label}
            </a>
        """
        return mark_safe(button_html)

    def preview_layer(self, obj):
        label = _("Preview Layer")
        button_html = f"""
            <a href="{obj.preview_url}" class="button button-small button--icon button-secondary">
                <span class="icon-wrapper">
                    <svg class="icon icon-plus icon" aria-hidden="true">
                        <use href="#icon-view"></use>
                    </svg>
                </span>
                {label}
            </a>
        """
        return mark_safe(button_html)

    def uploaded_files(self, obj):
        label = _("Uploaded Files")
        button_html = f"""
            <a href="{obj.get_uploads_list_url()}" class="button button-small button--icon bicolor button-secondary">
                <span class="icon-wrapper">
                    <svg class="icon icon-list-ol icon" aria-hidden="true">
                        <use href="#icon-list-ol"></use>
                    </svg>
                </span>
                {label}
            </a>
        """
        return mark_safe(button_html)


class MBTSourceModelAdmin(ModelAdminCanHide):
    model = MBTSource
    menu_label = _("Basemap Sources")
    menu_icon = "globe"
    form_view_extra_js = ["geomanager/js/mbt_source_extra.js"]


class LayerRasterFileModelAdmin(ModelAdminCanHide):
    model = LayerRasterFile
    exclude_from_explorer = True
    hidden = True
    list_display = ("__str__", "layer", "time",)
    list_filter = ("layer",)
    index_template_name = "modeladmin/index_without_custom_create.html"


class PgVectorTableModelAdmin(ModelAdminCanHide):
    model = PgVectorTable
    hidden = True
    list_display = ("__str__", "table_name",)
    list_filter = ("layer",)
    index_template_name = "modeladmin/index_without_custom_create.html"
    inspect_view_enabled = True


class GeoManagerAdminGroup(ModelAdminGroupWithHiddenItems):
    menu_label = _('Geo Manager')
    menu_icon = 'layer-group'
    menu_order = 700
    items = (
        CategoryModelAdmin,
        DatasetModelAdmin,
        MetadataModelAdmin,
        RasterFileLayerModelAdmin,
        RasterStyleModelAdmin,
        VectorFileLayerModelAdmin,
        WmsLayerModelAdmin,
        RasterTileLayerModelAdmin,
        VectorTileLayerModelAdmin,
        MBTSourceModelAdmin,
        LayerRasterFileModelAdmin,
        PgVectorTableModelAdmin
    )

    def get_submenu_items(self):
        menu_items = super().get_submenu_items()

        try:
            settings_url = reverse(
                "wagtailsettings:edit",
                args=[AdminBoundarySettings._meta.app_label, AdminBoundarySettings._meta.model_name, ],
            )
            abm_settings_menu = MenuItem(label=_("Boundary Settings"), url=settings_url, icon_name="cog")
            menu_items.append(abm_settings_menu)
        except Exception:
            pass

        boundary_loader = MenuItem(label=_("Boundary Data"), url=reverse("adminboundarymanager_preview_boundary"),
                                   icon_name="map")
        menu_items.append(boundary_loader)

        stations_data = MenuItem(label=_("Stations Data"), url=reverse("geomanager_preview_stations"),
                                 icon_name="map")
        menu_items.append(stations_data)

        try:
            settings_url = reverse(
                "wagtailsettings:edit",
                args=[GeomanagerSettings._meta.app_label, GeomanagerSettings._meta.model_name, ],
            )
            gm_settings_menu = MenuItem(label=_("Settings"), url=settings_url, icon_name="cog")
            menu_items.append(gm_settings_menu)
        except Exception:
            pass

        return menu_items


modeladmin_register(GeoManagerAdminGroup)


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        'wagtailfontawesomesvg/solid/palette.svg',
        'wagtailfontawesomesvg/solid/database.svg',
        'wagtailfontawesomesvg/solid/layer-group.svg',
        'wagtailfontawesomesvg/solid/globe.svg',
        'wagtailfontawesomesvg/solid/map.svg',
    ]


@hooks.register('construct_settings_menu')
def hide_settings_menu_item(request, menu_items):
    hidden_settings = ["admin-boundary-settings", "geomanager-settings"]
    menu_items[:] = [item for item in menu_items if item.name not in hidden_settings]
