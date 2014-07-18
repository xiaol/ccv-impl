from django.conf.urls import patterns, include, url
import os
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

handler404 = 'videoCMS.views.channel.index'

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__),'templates').replace('\\','/')}),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__),'static').replace('\\','/')}),
    url(r'^admin/(.*)$','admin.site.root'),
    #url(r'^$','videoCMS.views.channel.index'),
    url(r'^$', 'videoCMS.views.weixin.index.index'),
    url(r'^search/$', include('haystack.urls')),
    url(r'^login$', 'videoCMS.views.login.login'),
    url(r'^logout$', 'videoCMS.views.login.logout'),
    
    url(r'^category/index$', 'videoCMS.views.category.index'),
    url(r'^category/add$', 'videoCMS.views.category.add'),
    url(r'^category/update$', 'videoCMS.views.category.update'),
    url(r'^category/resetWeight$', 'videoCMS.views.category.resetWeight'),
    url(r'^category/showJson$', 'videoCMS.views.category.showJson'),
    
    url(r'^channel/index$', 'videoCMS.views.channel.index'),
    url(r'^channel/add$', 'videoCMS.views.channel.add'),
    url(r'^channel/update$', 'videoCMS.views.channel.update'),
    url(r'^channel/updateDuration$', 'videoCMS.views.channel.updateDuration'),
    url(r'^channel/delete$', 'videoCMS.views.channel.deleteChannel'),
    url(r'^channel/updateSearchNow$', 'videoCMS.views.channel.updateSearchNow'),
    url(r'^channel/detail$', 'videoCMS.views.channel.detail'),
    url(r'^channel/detail/extraDouban$', 'videoCMS.views.channel.detailExtraDouban'),
    url(r'^channel/resetWeight$', 'videoCMS.views.channel.resetWeight'),
    url(r'^channel/toggleProcessed$', 'videoCMS.views.channel.toggleProcessed'),
    url(r'^channel/toggleRec$', 'videoCMS.views.channel.toggleRec'),
    url(r'^channel/showJson$', 'videoCMS.views.channel.showJson'),
    url(r'^channel/search$', 'videoCMS.views.channel.search'),
    url(r'^channel/searchChannelId', 'videoCMS.views.channel.searchChannelId'),
    url(r'^channel/setCompleted$', 'videoCMS.views.channel.setCompleted'),
    url(r'^channel/disperseUpdateTime$', 'videoCMS.views.channel.disperseUpdateTime'),
    url(r'^channel/pushChannel$', 'videoCMS.views.channel.pushChannel'),


    
    url(r'^resource/index$', 'videoCMS.views.resource.index'),
    url(r'^resource/add$', 'videoCMS.views.resource.add'),
    url(r'^resource/getVideoId$', 'videoCMS.views.resource.getVideoId'),
    url(r'^resource/update$', 'videoCMS.views.resource.update'),
    url(r'^resource/toggleOnlineStatus$', 'videoCMS.views.resource.toggleOnlineStatus'),
    url(r'^resource/refreshSnapshot$', 'videoCMS.views.resource.refreshSnapshot'),
    url(r'^resource/delete$', 'videoCMS.views.resource.deleteResource'),
    url(r'^resource/deleteChannelResource$', 'videoCMS.views.resource.deleteChannelResource'),
    url(r'^resource/stopSnapshot$', 'videoCMS.views.resource.stopSnapshot'),
    url(r'^resource/prefetchCDN$', 'videoCMS.views.resource.prefetchCDN'),
    url(r'^resource/queryCDN$', 'videoCMS.views.resource.queryCDN'),
    url(r'^resource/showJson$', 'videoCMS.views.resource.showJson'),
    url(r'^resource/getVideoUrl$', 'videoCMS.views.resource.getVideoUrl'),
    url(r'^resource/unsetInvalid$', 'videoCMS.views.resource.unsetInvalid'),
    url(r'^resource/search$', 'videoCMS.views.resource.search'),
    url(r'^resource/searchResourceId', 'videoCMS.views.resource.searchId'),
    url(r'^resource/pushResource$', 'videoCMS.views.resource.pushResource'),
    url(r'^resource/batch_review$', 'videoCMS.views.resource.batch_review'),
    url(r'^resource/review$', 'videoCMS.views.resource.review'),
    url(r'^resource/lookupDanmu$', 'videoCMS.views.resource.lookupDanmu'),


    url(r'^resourceGif/add$', 'videoCMS.views.resource_gif.add'),
    url(r'^resourceGif/update$', 'videoCMS.views.resource_gif.update'),
    
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

    url(r'^statistics/category$','videoCMS.views.statistics.category'),
    url(r'^statistics/channel$','videoCMS.views.statistics.channel'),

    url(r'^statistics/channelSub$','videoCMS.views.statistics.channelSub'),
    url(r'^statistics2/channelSub2$','videoCMS.views.statistics2.channelSub2'),
    url(r'^statistics/autoResource$','videoCMS.views.statistics.autoResource'),
    url(r'^statistics/resource$','videoCMS.views.statistics.resource'),
    url(r'^statistics/kaifang$','videoCMS.views.statistics.kaifang'),

    url(r'^statistics2/category$','videoCMS.views.statistics2.category'),
    url(r'^statistics2/categoryDetail$','videoCMS.views.statistics2.categoryDetail'),
    url(r'^statistics2/channel$','videoCMS.views.statistics2.channel'),
    url(r'^statistics2/channelAjax$','videoCMS.views.statistics2.channelAjax'),
    url(r'^statistics2/resource$','videoCMS.views.statistics2.resource'),
    url(r'^statistics2/weiboUser$','videoCMS.views.statistics2.weiboUser'),
    url(r'^statistics2/search','videoCMS.views.statistics2.search'),
    url(r'^statistics2/playTime','videoCMS.views.statistics2.playTime'),
    url(r'^statistics2/apiFeed','videoCMS.views.statistics2.apiFeed'),
    url(r'^statistics2/appDownload','videoCMS.views.statistics2.appDownload'),


    url(r'^about$','videoCMS.views.about.index'),

    url(r'^message$', 'videoCMS.views.message.unread'),
    url(r'^message/readed$', 'videoCMS.views.message.readed'),
    url(r'^message/all$', 'videoCMS.views.message.all'),
    url(r'^message/flagRead$', 'videoCMS.views.message.flagRead'),
    url(r'^message/flagUnread', 'videoCMS.views.message.flagUnread'),
    url(r'^message/markMessage', 'videoCMS.views.message.markMessage'),
    url(r'^message/marked', 'videoCMS.views.message.marked'),


    url(r'^topic/index$', 'videoCMS.views.topic.index'),
    url(r'^topic/add$', 'videoCMS.views.topic.add'),
    url(r'^topic/update$', 'videoCMS.views.topic.update'),
    url(r'^topic/resetWeight$', 'videoCMS.views.topic.resetWeight'),
    url(r'^topic/showJson$', 'videoCMS.views.topic.showJson'),
    url(r'^topic/addResourceToNewestBaBa', 'videoCMS.views.topic.addResourceToNewestBaBa'),
    url(r'^topic/toggleOnlineStatus$', 'videoCMS.views.topic.toggleOnlineStatus'),


    url(r'^setting/update$','videoCMS.views.setting.update'),


    url(r'^user/index$','videoCMS.views.user.index'),
    url(r'^user/edit','videoCMS.views.user.edit'),
    url(r'^user/add$','videoCMS.views.user.add'),
    url(r'^user/list$','videoCMS.views.user.list_'),

    url(r'^image/reco$','videoCMS.views.image.reco'),
)
