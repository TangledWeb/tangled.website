<%inherit file="/entry.mako" />

<%block name="page_title">Documentation</%block>

<%block name="content">
  ${parent.content()}
  <ul>
    % for link in links:
      <li><a href="${link['href']}">${link['text']}</a></li>
    % endfor
  </ul>
</%block>
