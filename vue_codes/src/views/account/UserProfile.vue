<template>
    <div class="container-fluid p-0">
      <div class="row" id="profile_info_pad" style="display:''">
        <div class="col-12 col-lg-12">
          <h1 class="h3 mb-3">{{$t('account_info')}}</h1>
          <div class="row">
            <div class="col-md-3 col-xl-2" >
              <div class="card">
                <div class="card-header"><h5 class="card-title mb-0">{{$t('profile_settings')}}</h5></div>
                <div class="list-group list-group-flush" role="tablist">
                  <a class="list-group-item list-group-item-action active" data-toggle="list" href="#account_info" role="tab">{{$t('account')}}</a>
                  <a class="list-group-item list-group-item-action" data-toggle="list" href="#password" role="tab">{{$t('password')}}</a>
                  <a class="list-group-item list-group-item-action" data-toggle="list" href="#mydata" role="tab">{{$t('my_data')}}</a>
                  <a class="list-group-item list-group-item-action" data-toggle="list" href="#delete_record" role="tab">{{$t('delete_account')}}</a>
                </div>
              </div>
            </div>
            <div class="col-md-9 col-xl-10">
              <div class="tab-content">
                <input type="hidden" id="act" value="modify" />
                <div class="tab-pane fade show active" id="account_info" role="tabpanel">
                  <div class="card">
                    <div class="card-header"><h5 class="card-title mb-0">{{$t('public_info')}}</h5></div>
                    <div class="card-body">
                      <div class="row">
                        <div class="col-md-8">
                          <div class="form-group">
                            <label class="col-form-label">Code</label>
                            <input type="text" id="code" value="U156973967553" class="form-control" readonly />
                          </div>
                          <div class="form-group">
                            <label class="col-form-label">ID</label>
                            <input type="text" id="id" value="hanskim" class="form-control" />
                          </div>
                          <div class="form-group">
                            <label class="col-form-label">Email</label>
                            <input type="text" id="email" value="hans@nicehans.com" class="form-control" />
                          </div>
                          <div class="form-row">
                            <div class="form-group col-md-3">
                              <label>Database</label>
                              <select id="db_name" class="form-control">
                                <option value="none">none</option>
                                <option value="SH_Test">SH_Test</option>
                                <option value="TSD">TSD</option>
                                <option value="cnt_demo" selected>cnt_demo</option>
                                <option value="dvo">dvo</option>
                              </select>
                            </div>
                            <div class="form-group col-md-5">
                              <label>Role</label>
                              <div class="form-group mb-0">
                                <label class="form-check-inline mt-1">
                                  <input class="form-check-input" type="radio" name="role" value="admin" checked />
                                  <span class="form-check-label">Admin</span>
                                </label>
                                <label class="form-check-inline mt-1">
                                  <input class="form-check-input" type="radio" name="role" value="poweruser" />
                                  <span class="form-check-label">Power User</span>
                                </label>
                                <label class="form-check-inline mt-1">
                                  <input class="form-check-input" type="radio" name="role" value="user" />
                                  <span class="form-check-label">User</span>
                                </label>
                                <label class="form-check-inline mt-1">
                                  <input class="form-check-input" type="radio" name="role" value="guest" />
                                  <span class="form-check-label">Guest</span>
                                </label>
                              </div>
                            </div>
                            <div class="form-group col-md-3">
                              <label>Flag</label>
                              <div class="form-group mb-0">
                                <label class="form-check-inline mt-1">
                                  <input class="form-check-input" type="radio" name="flag" value="y" checked />
                                  <span class="form-check-label">Activate</span>
                                </label>
                                <label class="form-check-inline mt-1">
                                  <input class="form-check-input" type="radio" name="flag" value="n" />
                                  <span class="form-check-label">Disabled</span>
                                </label>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div class="col-md-4">
                          <div class="text-center">
                            <img id="img_view" src="" class="rounded-circle img-responsive mt-2" width="300" height="300" />
                          </div> 
                        </div>
                      </div>
                      <button type="submit" name="btn" class="btn btn-primary" value="public" onClick="saveUserInfo(this)">Save</button>
                    </div>
                  </div>
                  <div class="card">
                    <div class="card-header"><h5 class="card-title mb-0">Private info</h5></div>
                    <div class="card-body">
                      <div class="form-row">
                        <div class="form-group col-md-6">
                          <label class="col-form-label">Name</label>
                          <input type="text" id="name" value="Hans Kim" class="form-control" />
                        </div>
                        <div class="form-group col-md-6">
                          <label class="col-form-label">English Name</label>
                          <input type="text" id="name_eng" value="Hans Kim" class="form-control" />
                        </div>
                      </div>
                      <div class="form-row">
                        <div class="form-group col-md-3">
                          <label class="col-form-label">Telephone</label>
                          <input type="text" id="telephone" value="+86-1802530 5107" class="form-control" />
                        </div>
                        <div class="form-group col-md-9">
                          <label class="col-form-label">Address</label>
                            <input type="text" id="address" value="广东深圳深圳龙岗区坂田街道河背村新河街8号金禾大厦8楼" class="form-control">
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="col-form-label">Address Detail</label>
                          <input type="text" id="address_b" value="" class="form-control" />
                        </div>
                        <button type="submit" name="btn" class="btn btn-primary" value="private" onClick="saveUserInfo(this)">Save</button>
                      </div>
                    </div>
                  </div>
                  <div class="tab-pane fade" id="password" role="tabpanel">
                    <div class="card">
                      <div class="card-header"><h5 class="card-title">Password</h5></div>
                      <div class="card-body">
                        <div class="form-group">
                          <label class="col-form-label">Current password</label>
                          <input type="text" id="current_pw" value="" class="form-control" />
                        </div>
                        <div class="form-group">
                          <label class="col-form-label">New password</label>
                          <input type="text" id="new_pw1" value="" class="form-control" />
                        </div>
                        <div class="form-group">
                          <label class="col-form-label">Verify password</label>
                          <input type="text" id="new_pw2" value="" class="form-control" />
                        </div>
                        <button type="submit" name="btn" class="btn btn-primary" value="passwd" onClick="saveUserInfo(this)">Save</button>
                        </div>
                      </div>
                    </div>
                    <div class="tab-pane fade" id="mydata" role="tabpanel">
                      <div class="card">
                        <div class="card-header"><h5 class="card-title">My data</h5></div>
                        <div class="card-body">
                          <div class="form-row">
                            <div class="form-group col-md-5">
                              <label>Language</label>
                              <div class="form-group mb-0">
                                <label class="form-check-inline mt-1">
                                  <input class="form-check-input" type="radio" name="language" value="chi" checked />
                                  <span class="form-check-label">中文</span>
                                </label>
                                <label class="form-check-inline mt-1">
                                  <input class="form-check-input" type="radio" name="language" value="eng" />
                                  <span class="form-check-label">English</span>
                                </label>
                                <label class="form-check-inline mt-1">
                                  <input class="form-check-input" type="radio" name="language" value="kor" />
                                  <span class="form-check-label">한국어</span>
                                </label>
                                <label class="form-check-inline mt-1">
                                  <input class="form-check-input" type="radio" name="language" value="fre" />
                                  <span class="form-check-label">French</span>
                                </label>
                              </div>
                            </div>
                          </div>
                          <div class="form-row">
                            <div class="form-group col-md-6">
                              <label class="col-form-label">Date In</label>
                              <input type="text" id="date_in" value="2019-09-30" class="form-control" />
                            </div>
                            <div class="form-group col-md-6">
                              <label class="col-form-label">Date Out</label>
                              <input type="text" id="date_out" value="2019-09-30" class="form-control" />
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="col-form-label">Comment</label>
                            <textarea id="comment" class="form-control"></textarea>
                          </div>
                        <div class="form-group">
                          <label class="form-label w-100">Image File</label>
                          <input type="file" name="imgfile" id="img_file" accept="image/*" />
                          <small class="form-text text-muted">img file such as .jpg, .png under 2M Byte</small>
                        </div>
                        <button type="submit" name="btn" class="btn btn-primary" value="mydata" onClick="saveUserInfo(this)">Save</button>
                      </div>
                    </div>
                  </div>
                  <div class="tab-pane fade" id="delete_record" role="tabpanel">
                    <div class="card">
                      <div class="card-header"><h5 class="card-title">Delete Account</h5></div>
                      <div class="card-body">
                      <div class="form-group"><p class="mb-0">Are you sure to delete this record?</p></div>
                      <div class="form-group">
                        <label>Password</label>
                        <input type="password" id="passwd" class="form-control" />
                        <small class="form-text text-muted">Type Admin password</small> 
                      </div>
                      <button type="submit" name="btn" class="btn btn-warning" value="delete" onClick="saveUserInfo(this)">Delete Account</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  
</template>