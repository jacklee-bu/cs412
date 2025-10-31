# File: views.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: October 2025
# Description: Views for voter_analytics app

from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models import Q


class VoterListView(ListView):
    """View to display a list of voters with filtering capabilities."""
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100  # show 100 voters per page

    def get_queryset(self):
        """Filter the queryset based on form parameters."""
        # start with all voters
        queryset = super().get_queryset()

        # get filter parameters from the GET request
        party = self.request.GET.get('party')
        min_dob_year = self.request.GET.get('min_dob')
        max_dob_year = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')

        # filter by party affiliation if provided
        if party:
            queryset = queryset.filter(party_affiliation=party)

        # filter by minimum date of birth year
        if min_dob_year:
            # voters born after or in this year
            queryset = queryset.filter(date_of_birth__year__gte=int(min_dob_year))

        # filter by maximum date of birth year
        if max_dob_year:
            # voters born before or in this year
            queryset = queryset.filter(date_of_birth__year__lte=int(max_dob_year))

        # filter by voter score
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))

        # filter by specific elections
        if self.request.GET.get('v20state'):
            queryset = queryset.filter(v20state=True)
        if self.request.GET.get('v21town'):
            queryset = queryset.filter(v21town=True)
        if self.request.GET.get('v21primary'):
            queryset = queryset.filter(v21primary=True)
        if self.request.GET.get('v22general'):
            queryset = queryset.filter(v22general=True)
        if self.request.GET.get('v23town'):
            queryset = queryset.filter(v23town=True)

        # order by last name, then first name for consistent ordering
        return queryset.order_by('last_name', 'first_name')

    def get_context_data(self, **kwargs):
        """Add filter form data to the context."""
        context = super().get_context_data(**kwargs)

        # get all unique party affiliations for the dropdown
        parties = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')
        context['parties'] = parties

        # create year range for birth year dropdowns
        # find the min and max birth years
        min_year = Voter.objects.order_by('date_of_birth').first().date_of_birth.year if Voter.objects.exists() else 1900
        max_year = Voter.objects.order_by('-date_of_birth').first().date_of_birth.year if Voter.objects.exists() else 2023
        context['year_range'] = range(min_year, max_year + 1)

        # voter scores 0-5
        context['voter_scores'] = range(6)

        # maintain filter values in the form
        context['selected_party'] = self.request.GET.get('party', '')
        context['selected_min_dob'] = self.request.GET.get('min_dob', '')
        context['selected_max_dob'] = self.request.GET.get('max_dob', '')
        context['selected_voter_score'] = self.request.GET.get('voter_score', '')
        context['v20state_checked'] = self.request.GET.get('v20state', '')
        context['v21town_checked'] = self.request.GET.get('v21town', '')
        context['v21primary_checked'] = self.request.GET.get('v21primary', '')
        context['v22general_checked'] = self.request.GET.get('v22general', '')
        context['v23town_checked'] = self.request.GET.get('v23town', '')

        return context


class VoterDetailView(DetailView):
    """View to display details for a single voter."""
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

    def get_context_data(self, **kwargs):
        """Add Google Maps link to context."""
        context = super().get_context_data(**kwargs)

        # create Google Maps URL for the voter's address
        voter = self.object
        address = voter.full_address
        # encode the address for URL
        import urllib.parse
        encoded_address = urllib.parse.quote(address)
        context['google_maps_url'] = f"https://www.google.com/maps/search/?api=1&query={encoded_address}"

        return context


class GraphsView(ListView):
    """View to display graphs of voter data."""
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        """Filter the queryset based on form parameters."""
        # start with all voters
        queryset = super().get_queryset()

        # get filter parameters from the GET request
        party = self.request.GET.get('party')
        min_dob_year = self.request.GET.get('min_dob')
        max_dob_year = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')

        # filter by party affiliation if provided
        if party:
            queryset = queryset.filter(party_affiliation=party)

        # filter by minimum date of birth year
        if min_dob_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_dob_year))

        # filter by maximum date of birth year
        if max_dob_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_dob_year))

        # filter by voter score
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))

        # filter by specific elections
        if self.request.GET.get('v20state'):
            queryset = queryset.filter(v20state=True)
        if self.request.GET.get('v21town'):
            queryset = queryset.filter(v21town=True)
        if self.request.GET.get('v21primary'):
            queryset = queryset.filter(v21primary=True)
        if self.request.GET.get('v22general'):
            queryset = queryset.filter(v22general=True)
        if self.request.GET.get('v23town'):
            queryset = queryset.filter(v23town=True)

        return queryset

    def get_context_data(self, **kwargs):
        """Generate graphs and add to context."""
        context = super().get_context_data(**kwargs)

        # import plotly for graphing
        import plotly.graph_objects as go
        import plotly.io as pio
        from django.db.models import Count

        # get the filtered queryset
        voters = self.get_queryset()

        # Graph 1: Birth Year Distribution
        # count voters by birth year
        birth_years = {}
        for voter in voters:
            year = voter.date_of_birth.year
            if year in birth_years:
                birth_years[year] += 1
            else:
                birth_years[year] = 1

        # sort years for the graph
        sorted_years = sorted(birth_years.keys())
        year_counts = [birth_years[year] for year in sorted_years]

        # create the birth year histogram
        fig_birth = go.Figure(data=[
            go.Bar(x=sorted_years, y=year_counts)
        ])
        fig_birth.update_layout(
            title='Voter Distribution by Year of Birth',
            xaxis_title='Year of Birth',
            yaxis_title='Number of Voters',
            showlegend=False
        )

        # Graph 2: Party Affiliation Pie Chart
        # count voters by party
        party_counts = voters.values('party_affiliation').annotate(count=Count('id'))
        parties = [p['party_affiliation'] for p in party_counts]
        counts = [p['count'] for p in party_counts]

        # create the pie chart
        fig_party = go.Figure(data=[
            go.Pie(labels=parties, values=counts)
        ])
        fig_party.update_layout(
            title='Voter Distribution by Party Affiliation'
        )

        # Graph 3: Election Participation
        # count participation in each election
        election_data = {
            '2020 State': voters.filter(v20state=True).count(),
            '2021 Town': voters.filter(v21town=True).count(),
            '2021 Primary': voters.filter(v21primary=True).count(),
            '2022 General': voters.filter(v22general=True).count(),
            '2023 Town': voters.filter(v23town=True).count(),
        }

        # create the election participation bar chart
        fig_elections = go.Figure(data=[
            go.Bar(x=list(election_data.keys()), y=list(election_data.values()))
        ])
        fig_elections.update_layout(
            title='Voter Participation by Election',
            xaxis_title='Election',
            yaxis_title='Number of Voters',
            showlegend=False
        )

        # convert figures to HTML
        context['birth_year_graph'] = fig_birth.to_html(full_html=False, include_plotlyjs='cdn')
        context['party_graph'] = fig_party.to_html(full_html=False, include_plotlyjs=False)
        context['elections_graph'] = fig_elections.to_html(full_html=False, include_plotlyjs=False)

        # add filter form data
        # get all unique party affiliations for the dropdown
        all_parties = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')
        context['parties'] = all_parties

        # create year range for birth year dropdowns
        min_year = Voter.objects.order_by('date_of_birth').first().date_of_birth.year if Voter.objects.exists() else 1900
        max_year = Voter.objects.order_by('-date_of_birth').first().date_of_birth.year if Voter.objects.exists() else 2023
        context['year_range'] = range(min_year, max_year + 1)

        # voter scores 0-5
        context['voter_scores'] = range(6)

        # maintain filter values in the form
        context['selected_party'] = self.request.GET.get('party', '')
        context['selected_min_dob'] = self.request.GET.get('min_dob', '')
        context['selected_max_dob'] = self.request.GET.get('max_dob', '')
        context['selected_voter_score'] = self.request.GET.get('voter_score', '')
        context['v20state_checked'] = self.request.GET.get('v20state', '')
        context['v21town_checked'] = self.request.GET.get('v21town', '')
        context['v21primary_checked'] = self.request.GET.get('v21primary', '')
        context['v22general_checked'] = self.request.GET.get('v22general', '')
        context['v23town_checked'] = self.request.GET.get('v23town', '')

        return context