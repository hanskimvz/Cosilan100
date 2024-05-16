<template>
		<div class="container-fluid p-0">
			<div class="row">
				<div class="col-lg-6 col-xl-5">
					<div class="row w-100">
						<div class="col-sm-6">
							<div class="card flex-fill">
								<div class="card-header">
									<span id="card[0][badge]" class="badge float-right" style="background-color:#47bac1">Visitors</span>
									<h5 id="card[0][title]" class="card-title mb-0">Today</h5>{{ $route.meta.page }}
								</div>
								<div class="card-body my-2">
									<div class="row d-flex align-items-center mb-4">
										<div class="col-8">
											<h2 id="card[0][value]" class="d-flex align-items-center mb-0 font-weight-light">0</h2>
										</div>
										<div class="col-4 text-right"><span id="card[0][percent]" class="text-muted">100%</span></div>
									</div>
									<div class="progress progress-sm shadow-sm mb-1">
										<div id="card[0][progress]" class="progress-bar" role="progressbar"
											style="width:100%; background-color:#47bac1"></div>
									</div>
								</div>
							</div>
							<div class="card flex-fill">
								<div class="card-header">
									<span id="card[2][badge]" class="badge float-right" style="background-color:#5b7dff">Visitors</span>
									<h5 id="card[2][title]" class="card-title mb-0">12 Weeks Average</h5>
								</div>
								<div class="card-body my-2">
									<div class="row d-flex align-items-center mb-4">
										<div class="col-8">
											<h2 id="card[2][value]" class="d-flex align-items-center mb-0 font-weight-light">0</h2>
										</div>
										<div class="col-4 text-right"><span id="card[2][percent]" class="text-muted">100%</span></div>
									</div>
									<div class="progress progress-sm shadow-sm mb-1">
										<div id="card[2][progress]" class="progress-bar" role="progressbar"
											style="width:100%; background-color:#5b7dff"></div>
									</div>
								</div>
							</div>
						</div>
						<div class="col-sm-6">
							<div class="card flex-fill">
								<div class="card-header">
									<span id="card[1][badge]" class="badge float-right" style="background-color:#fcc100">Visitors</span>
									<h5 id="card[1][title]" class="card-title mb-0">Yesterday</h5>
								</div>
								<div class="card-body my-2">
									<div class="row d-flex align-items-center mb-4">
										<div class="col-8">
											<h2 id="card[1][value]" class="d-flex align-items-center mb-0 font-weight-light">0</h2>
										</div>
										<div class="col-4 text-right"><span id="card[1][percent]" class="text-muted">100%</span></div>
									</div>
									<div class="progress progress-sm shadow-sm mb-1">
										<div id="card[1][progress]" class="progress-bar" role="progressbar"
											style="width:100%; background-color:#fcc100"></div>
									</div>
								</div>
							</div>
							<div class="card flex-fill">
								<div class="card-header">
									<span id="card[3][badge]" class="badge float-right" style="background-color:#5fc27e">Visitors</span>
									<h5 id="card[3][title]" class="card-title mb-0">12 Weeks Total</h5>
								</div>
								<div class="card-body my-2">
									<div class="row d-flex align-items-center mb-4">
										<div class="col-8">
											<h2 id="card[3][value]" class="d-flex align-items-center mb-0 font-weight-light">0</h2>
										</div>
										<div class="col-4 text-right"><span id="card[3][percent]" class="text-muted">100%</span></div>
									</div>
									<div class="progress progress-sm shadow-sm mb-1">
										<div id="card[3][progress]" class="progress-bar" role="progressbar"
											style="width:100%; background-color:#5fc27e"></div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div class="col-lg-6 col-xl-7">
					<div class="card flex-fill w-100 d-flex">
						<div class="card-header">
							<h5 class="card-title mb-0" id="footfall_title">Footfall</h5>
						</div>
						<div class="card-body  p-2">
							<div id="footfall_bar_chart"></div>
							<div id="footfall_curve_chart"></div>
						</div>
					</div>
				</div>
			</div>
			<div class="row" id="third_block"></div>
		</div>
</template>

<script setup>

</script>

<style></style>