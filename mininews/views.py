from django.views.generic.dates import ArchiveIndexView, YearArchiveView
from django.views.generic import DetailView


class GetQuerysetMixin(object):

    mininews_live = ('published',)

    def get_queryset(self):
        qs = super(GetQuerysetMixin, self).get_queryset()
        # Staff users are a special case - we want them to be able to see an article
        # (most) of the time, so that they can review it before it goes live.
        # The exception is when an article can have extra statuses - e.g. draft, published,
        # archived. In this case, we only want the show the status that is applicable to
        # this page, *plus* the draft status.
        if self.request.user.is_authenticated() and self.request.user.is_staff:
            staff_statuses = self.mininews_live + (self.model.STATUS.draft,)
            return qs.filter(status__in=staff_statuses)
        return qs.live(statuses=self.mininews_live)


class MininewsArchiveIndexView(GetQuerysetMixin, ArchiveIndexView):
    date_field = 'start'


class MininewsYearArchiveView(GetQuerysetMixin, YearArchiveView):
    date_field = 'start'


class MininewsDetailView(GetQuerysetMixin, DetailView):
    pass
