<template>
  <div class="form-inline d-none d-sm-inline-block">
    <input type = "hidden" id="view_by" value="hour" />
    <input type = "hidden" id="fr" value="dashboard" />
    <select class="form-control mr-sm-2" id="square" OnChange="changeSpot(0);"><option value="0">All Square</option></select>
    <select class="form-control mr-sm-2" id="store" OnChange="changeStore(0);"><option value="0">All Store</option></select>
    <span class="ml-3"></span>
    <span class="ml-2" id="date_additional" style="display:none">
      <span type="button" class="form-control" OnClick="changeDate(-2);"><i class="fa fa-chevron-left"></i></span>
      <input type="text" class="form-control form-control-no-border mr-sm-6 text-center" name="refdate_from" id="refdate_from" size="10" OnChange="changeDate(0)" />
      <span type="button" class="form-control" OnClick="changeDate(2);"><i class="fa fa-chevron-right"></i></span>
      <span class="ml-2 mr-2">~</span>
    </span>
    <span type="button" class="form-control" OnClick="changeDate(-1);"><i class="fa fa-chevron-left"></i></span>
    <input type="text" class="form-control form-control-no-border mr-sm-6 text-center" name="refdate" id="refdate" size="10" OnChange="changeDate(0)" />
    <span type="button" class="form-control" OnClick="changeDate(1);"><i class="fa fa-chevron-right"></i></span>
  </div>
</template>