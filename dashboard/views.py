from django.shortcuts import render
from dashboard.models import Claim, ClaimDetail, ClaimNote;
from django.utils import timezone;
from django.core.paginator import Paginator;
# Create your views here.
def index(request):
    selected = None
    claim_details_param = request.GET.get("claim_details")
    if claim_details_param is not None:
        selected = ClaimDetail.objects.get(claim=claim_details_param)
    (_, claims) = get_claims_from_paginator(1)
    return render(request, "index.html", {
        "claims": claims,
        "claim_details": selected,
        "current_page": 1,
    })

# Returns (int, Page), first return value is the updated page number in case the one given was invalid.
def get_claims_from_paginator(page, search = None, status_filter = None):
    if page == None:
        page = 1
    else:
        page = int(page)
    claim_objects = Claim.objects.all().order_by("id")
    if status_filter != None and status_filter != "":
        claim_objects = claim_objects.filter(status=status_filter)
    if search != None and search != "":
        search_patient_name = claim_objects.filter(patient_name__icontains=search).values()
        new_claim_objects = search_patient_name
        search_insurer_name = claim_objects.filter(insurer_name__icontains=search).values()
        new_claim_objects |= search_insurer_name
        # Attempt to parse `search` as String, otherwise combine patient & insurer search.
        try:
            search_id = claim_objects.filter(id__icontains=int(search)).values()
            new_claim_objects |= search_id
        except ValueError:
            pass
        claim_objects = new_claim_objects
    
    paginator = Paginator(claim_objects, MAX_CLAIMS_PER_PAGE)
    page = max(1, min(page, paginator.num_pages))
    return (page, paginator.get_page(page))

MAX_CLAIMS_PER_PAGE = 10
def get_claims_table_page_view(request):
    search = request.POST.get("search")
    status_filter = request.POST.get("status_filter")
    (page, claims) = get_claims_from_paginator(request.POST.get("page"), search, status_filter)
    return render(request, "claims_table.html", {
        "current_page": page,
        "claims": claims,
        "current_search": search,
        "status_filter": status_filter
    })

def get_claim_details(request):
    print(request.GET.dict())
    claim = request.GET.get("claim_details")
    return render(request, "claim_details.html", {
        "claim_details": ClaimDetail.objects.get(claim = claim),
        "claim_notes": ClaimNote.objects.filter(claim = claim)
    })

def add_note(request):
    print(request.POST.dict())
    
    claim = Claim.objects.get(id=request.POST.get("claim"))
    note = ClaimNote.objects.create(claim = claim, content = request.POST.get("note_message"), is_review_flag = request.POST.get("is_review_flag") == 'true')
    note.save()
    return render(request, "claim_item.html", {
        "claim": claim,
        "claim_notes": ClaimNote.objects.filter(claim = claim),
        "update_claim_notes": True
    })