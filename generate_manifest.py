from iiif_prezi.factory import ManifestFactory

fac = ManifestFactory()
# Where the resources live on the web
fac.set_base_prezi_uri("http://www.example.org/path/to/object/")
# Where the resources live on disk
fac.set_base_prezi_dir("/home/user/web_root/path/to/object/")

# Default Image API information
fac.set_base_image_uri("http://www.example.org/path/to/image/api/")
fac.set_iiif_image_info(2.0, 2)  # Version, ComplianceLevel

# 'warn' will print warnings, default level
# 'error' will turn off warnings
# 'error_on_warning' will make warnings into errors
fac.set_debug("warn")
