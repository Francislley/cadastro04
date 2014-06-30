# coding: utf-8
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Campaign
from .forms import CampaignForm

@login_required
def create_campaign(request):
	created = False
	if request.method == 'POST':
		campaign_form = CampaignForm(request.POST, request.FILES)
		if campaign_form.is_valid():
			cf = campaign_form.save(commit=False)
			cf.user = request.user
			cf.save()
			created = True
		else:
			print(campaign_form.errors)
	else:
		campaign_form = CampaignForm()
	return render(request, 'campaign/create_campaign.html', {'campaign_form': campaign_form, 'created': created})

def list_campaign(request):
	list_camp = Campaign.objects.all().order_by('-created_at')
	paginator = Paginator(list_camp, 5)
	page = request.GET.get('page')
	try:
		list_campaign = paginator.page(page)
	except PageNotAnInteger:
		list_campaign = paginator.page(1)
	except EmptyPage:
		list_campaign = paginator.page(paginator.num_pages)
	return render(request, 'campaign/list_campaign.html', {'list_campaign': list_campaign})

def details(request, id):
	camp_destails = get_object_or_404(Campaign, id=id)
	return render(request, 'campaign/list_campaign_detais.html', {'camp_destails': camp_destails})