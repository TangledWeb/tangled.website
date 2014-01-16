<%inherit file="/base.mako" />

<%block name="page_title">Documentation</%block>

<%block name="content">
  <ul>
    % for link in links:
      <li><a href="${link['href']}">${link['text']}</a></li>
    % endfor
  </ul>
</%block>
