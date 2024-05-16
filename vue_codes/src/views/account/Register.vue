<template>
  <main class="main h-100 w-100">
		<div class="container h-100">
			<div class="row h-100">
				<div class="col-sm-10 col-md-8 col-lg-6 mx-auto d-table h-100">
					<div class="d-table-cell align-middle">
						<div class="text-center mt-4">
							<h1 class="h2">欢迎</h1>
							<p class="lead">开通新帐号</p>
						</div>
						<div class="card">
							<div class="card-body">
								<div class="m-sm-4">
									<div class="text-center">
									<span><i class="align-middle" style="width:60px; height:60px; color:#f000f0" data-feather="activity"></i></span>
										<!--img src="img/avatars/avatar.jpg" alt="Chris Wood" class="img-fluid rounded-circle" width="132" height="132" /-->
									</div>
									<form name="registerForm" method="POST" ENCTYPE="multipart/form-data">
										<div class="form-group">
											<label>帐号</label>
											<input class="form-control form-control-lg" type="text" name="ID" id="ID" placeholder="Enter ID"  value="" />
										</div>
										<div class="form-group">
											<label>邮箱</label>
											<input class="form-control form-control-lg" type="text" name="email" id="email" placeholder="Enter Email" value="" />
										</div>
										<div class="form-group">
											<label>密码</label>
											<input class="form-control form-control-lg" type="password" name="password" id="password" autocomplete="off" placeholder="Enter your password" />
										</div>
										<div class="form-group">
											<label>再输入密码</label>
											<input class="form-control form-control-lg" type="password" name="password2" id="password2"  autocomplete="off" placeholder="Retype your password" />
										</div>
										<div class="form-row">
											<div class="form-group col-md-6">
												<label>语言</label>
												<select class="form-control pull-right" name="language" OnChange="changeLanguage(this)" id="language">
													<option value="chi" selected>中文</option>
													<option value="eng" >English</option>
													<option value="kor" >한국어</option></select> 
											</div>
										</div>
										<div class="text-center mt-3">
											<button type="button" class="btn btn-lg btn-primary col-md-3 mt-2" name="register" OnClick="submitForm(this)"">开帐号</button>
										</div>
									</form>
								</div>
								<div class="m-sm-4">已有帐号？ <a href="admin.php?fr=login">按这里登录</a></div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</main>


</template>