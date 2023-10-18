<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>IPyWidget export</title>
</head>
<body>


<!-- Load require.js. Delete this if your page already loads require.js -->
<script src="//g.alicdn.com/aie/jp-notebook/{asset_version}/static/components/jquery/dist/jquery.min.js"></script>
<link rel="stylesheet" href="//g.alicdn.com/aie/jp-notebook/{asset_version}/static/components/jquery/dist/jquery-ui.min.css">
<script src="//g.alicdn.com/aie/jp-notebook/{asset_version}/static/components/jquery/dist/jquery-ui.min.js"></script>
<script src="//g.alicdn.com/aie/jp-notebook/{asset_version}/static/components/requirejs/require.js"></script>
<script src="//g.alicdn.com/aie/jp-notebook/{asset_version}/static/components/moment/min/moment.min.js"></script>
<link href="//g.alicdn.com/aie/jp-notebook/{asset_version}/static/build/theme.css" rel="stylesheet">

<style>
  #map {{
    height: 100% !important;
  }}
  .map-trigger {{
    display: none;
  }}
</style>

<script type="application/vnd.jupyter.widget-state+json">
{map}
</script>
<script type="application/vnd.jupyter.widget-view+json">
{view[0]}
</script>

<script>
  (function() {{
    function addWidgetsRenderer() {{
      var mimeElement = document.querySelector('script[type="application/vnd.jupyter.widget-view+json"]');
      var scriptElement = document.createElement('script');
      var widgetRendererSrc = "//g.alicdn.com/aie/jp-notebook/{asset_version}/@jupyter-widgets/html-manager/embed-amd.js";
      var widgetState;

      try {{
        widgetState = mimeElement && JSON.parse(mimeElement.innerHTML);

        if (widgetState && (widgetState.version_major < 2 || !widgetState.version_major)) {{
          widgetRendererSrc = '//g.alicdn.com/aie/jp-notebook/{asset_version}/jupyter-js-widgets@*/dist/embed.js';
        }}
      }} catch(e) {{}}

      scriptElement.src = widgetRendererSrc;
      document.body.appendChild(scriptElement);
    }}

    document.addEventListener('DOMContentLoaded', addWidgetsRenderer);
  }}());
    window.API_SERVER_CONSOLE="https://pre-engine-aiearth.aliyun.com";
</script>

<div id="map"></div>

</body>
</html>