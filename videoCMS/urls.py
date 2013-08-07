from django.conf.urls import patterns, include, url
import os
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__),'templates').replace('\\','/')}),
    
    url(r'^login$', 'videoCMS.views.login.login'),
    
    url(r'^category/index$', 'videoCMS.views.category.index'),
    url(r'^category/add$', 'videoCMS.views.category.add'),
    url(r'^category/update$', 'videoCMS.views.category.update'),
    url(r'^category/resetWeight$', 'videoCMS.views.category.resetWeight'),
    
    url(r'^channel/index$', 'videoCMS.views.channel.index'),
    url(r'^channel/add$', 'videoCMS.views.channel.add'),
    url(r'^channel/update$', 'videoCMS.views.channel.update'),
    url(r'^channel/updateDuration$', 'videoCMS.views.channel.updateDuration'),
    url(r'^channel/delete$', 'videoCMS.views.channel.deleteChannel'),
    url(r'^channel/updateSearchNow$', 'videoCMS.views.channel.updateSearchNow'),
    url(r'^channel/detail$', 'videoCMS.views.channel.detail'),
    url(r'^channel/detail/extraDouban$', 'videoCMS.views.channel.detailExtraDouban'),
    url(r'^channel/resetWeight$', 'videoCMS.views.channel.resetWeight'),
    
    url(r'^resource/index$', 'videoCMS.views.resource.index'),
    url(r'^resource/add$', 'videoCMS.views.resource.add'),
    url(r'^resource/getVideoId$', 'videoCMS.views.resource.getVideoId'),
    url(r'^resource/update$', 'videoCMS.views.resource.update'),
    url(r'^resource/toggleOnlineStatus$', 'videoCMS.views.resource.toggleOnlineStatus'),
    url(r'^resource/refreshSnapshot$', 'videoCMS.views.resource.refreshSnapshot'),
    url(r'^resource/delete$', 'videoCMS.views.resource.deleteResource'),
    url(r'^resource/stopSnapshot$', 'videoCMS.views.resource.stopSnapshot'),
    
    url(r'^preresource/index$', 'videoCMS.views.preresource.index'),
    url(r'^preresource/update$', 'videoCMS.views.preresource.update'),
    url(r'^preresource/addEd2k$', 'videoCMS.views.preresource.addEd2k'),
    url(r'^preresource/addBT$', 'videoCMS.views.preresource.addTorrent'),
    
    url(r'^tag/index$', 'videoCMS.views.tag.index'),
    url(r'^tag/add$', 'videoCMS.views.tag.add'),
    url(r'^tag/update$', 'videoCMS.views.tag.update'),
    
    url(r'^video/play','videoCMS.views.video.play'),
    
    
    url(r'^share/resource$','videoCMS.shareViews.resource.index'),
    url(r'^share/channel$','videoCMS.shareViews.channel.index'),
)
