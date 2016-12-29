<ul class="sidebar-menu">
    <li class="header">{{title}}</li>
    % for label, mpage in entries:
        <li class="{{'active' if label==active_page else ''}}">
            <a href="{{url(mpage.url)}}">
                <i class="{{mpage.icon}}"></i><span>{{mpage.title}}</span>
            </a>
        </li>
    % end
</ul>