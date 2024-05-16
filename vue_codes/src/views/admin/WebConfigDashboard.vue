<template>
  <div class="row">
    <div class="col-12"> <input type="hidden" id="label_list" value="entrance,exit,outside,none,">
      <div class="card">
        <div class="card-header">
          <h5 class="card-title mb-0">Card Banner</h5>
        </div>
        <div class="card-body">
          <table class="table table-striped table-sm table-bordered table-hover">
            <tbody>
              <tr>
                <th>PAGE</th>
                <th>title</th>
                <th>표시</th>
                <th>카운터 라벨</th>
                <th>badge</th>
                <th>color</th>
              </tr>
              <tr>
                <td class="text-center">
                  <table>
                    <tr>
                      <td style="background-color:#13f1fd"></td>
                      <td></td>
                    </tr>
                    <tr>
                      <td></td>
                      <td></td>
                    </tr>
                  </table>
                </td>
                <td><select class="form-control" id="card_banner[0][title]">
                    <option value="today" selected>today</option>
                    <option value="yesterday">yesterday</option>
                    <option value="average12week">average12week</option>
                    <option value="total12week">total12week</option>
                    <option value="average">average</option>
                    <option value="total">total</option>
                  </select></td>
                <td><input type="text" id="card_banner[0][display]" class="form-control" value="오늘"></td>
                <td><label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="card_banner[0][entrance]" checked><span
                      class="form-check-label">입구</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="card_banner[0][exit]"><span
                      class="form-check-label">출구</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="card_banner[0][outside]"><span
                      class="form-check-label">외부</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="card_banner[0][none]"><span
                      class="form-check-label">미설정</span></label> </td>
                <td><input type="text" id="card_banner[0][badge]" class="form-control" value="방문자수"></td>
                <td><input type="color" id="card_banner[0][color]" class="form-control" value="#47bac1"></td>
              </tr>
              <tr>
                <td class="text-center">
                  <table>
                    <tr>
                      <td></td>
                      <td style="background-color:#13f1fd"></td>
                    </tr>
                    <tr>
                      <td></td>
                      <td></td>
                    </tr>
                  </table>
                </td>
                <td><select class="form-control" id="card_banner[1][title]">
                    <option value="today">today</option>
                    <option value="yesterday" selected>yesterday</option>
                    <option value="average12week">average12week</option>
                    <option value="total12week">total12week</option>
                    <option value="average">average</option>
                    <option value="total">total</option>
                  </select></td>
                <td><input type="text" id="card_banner[1][display]" class="form-control" value="어제"></td>
                <td><label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="card_banner[1][entrance]" checked><span
                      class="form-check-label">입구</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="card_banner[1][exit]"><span
                      class="form-check-label">출구</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="card_banner[1][outside]"><span
                      class="form-check-label">외부</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="card_banner[1][none]"><span
                      class="form-check-label">미설정</span></label> </td>
                <td><input type="text" id="card_banner[1][badge]" class="form-control" value="방문자수"></td>
                <td><input type="color" id="card_banner[1][color]" class="form-control" value="#fcc100"></td>
              </tr>
              <tr>
                <td class="text-center">
                  <table>
                    <tr>
                      <td></td>
                      <td></td>
                    </tr>
                    <tr>
                      <td style="background-color:#13f1fd"></td>
                      <td></td>
                    </tr>
                  </table>
                </td>
                <td><select class="form-control" id="card_banner[2][title]">
                    <option value="today">today</option>
                    <option value="yesterday">yesterday</option>
                    <option value="average12week" selected>average12week</option>
                    <option value="total12week">total12week</option>
                    <option value="average">average</option>
                    <option value="total">total</option>
                  </select></td>
                <td><input type="text" id="card_banner[2][display]" class="form-control" value="12주평균"></td>
                <td><label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="card_banner[2][entrance]" checked><span
                      class="form-check-label">입구</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="card_banner[2][exit]"><span
                      class="form-check-label">출구</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="card_banner[2][outside]"><span
                      class="form-check-label">외부</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="card_banner[2][none]"><span
                      class="form-check-label">미설정</span></label> </td>
                <td><input type="text" id="card_banner[2][badge]" class="form-control" value="방문자수"></td>
                <td><input type="color" id="card_banner[2][color]" class="form-control" value="#5b7dff"></td>
              </tr>
              <tr>
                <td class="text-center">
                  <table>
                    <tr>
                      <td></td>
                      <td></td>
                    </tr>
                    <tr>
                      <td></td>
                      <td style="background-color:#13f1fd"></td>
                    </tr>
                  </table>
                </td>
                <td><select class="form-control" id="card_banner[3][title]">
                    <option value="today">today</option>
                    <option value="yesterday">yesterday</option>
                    <option value="average12week">average12week</option>
                    <option value="total12week" selected>total12week</option>
                    <option value="average">average</option>
                    <option value="total">total</option>
                  </select></td>
                <td><input type="text" id="card_banner[3][display]" class="form-control" value="12주전체"></td>
                <td><label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="card_banner[3][entrance]" checked><span
                      class="form-check-label">입구</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="card_banner[3][exit]"><span
                      class="form-check-label">출구</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="card_banner[3][outside]"><span
                      class="form-check-label">외부</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="card_banner[3][none]"><span
                      class="form-check-label">미설정</span></label> </td>
                <td><input type="text" id="card_banner[3][badge]" class="form-control" value="방문자수"></td>
                <td><input type="color" id="card_banner[3][color]" class="form-control" value="#5fc27e"></td>
              </tr>
            </tbody>
          </table>
          <button type="button" name="card_banner" class="btn btn-primary" value="card_banner"
            OnClick="changeOption(this)">저장</button>
          <span id="card_banner_result"></span>
        </div>
      </div>
      <div class="card">
        <div class="card-header">
          <h5 class="card-title mb-0">Footfall Section</h5>
        </div>
        <div class="card-body">
          <table class="table table-striped table-sm table-bordered table-hover">
            <tr>
              <td>Title</td>
              <td colspan="3"><input type="text" id="footfall_title" class="form-control" value="유동량"></td>
            </tr>
            <tr>
              <th>PAGE</th>
              <th>title</th>
              <th>표시</th>
              <th>카운터 라벨</th>
            </tr>
            <tr>
              <td>Bar Graph A</td>
              <td><select class="form-control" id="footfall[0][title]">
                  <option value="lastweek" selected>lastweek</option>
                  <option value="thisweek">thisweek</option>
                </select></td>
              <td><input type="text" id="footfall[0][display]" class="form-control" value="저번주"></td>
              <td><label class="form-check form-check-inline">
                  <input type="checkbox" class="form-check-input" id="footfall[0][entrance]" checked><span
                    class="form-check-label">입구</span></label> <label class="form-check form-check-inline">
                  <input type="checkbox" class="form-check-input" id="footfall[0][exit]"><span
                    class="form-check-label">출구</span></label> <label class="form-check form-check-inline">
                  <input type="checkbox" class="form-check-input" id="footfall[0][outside]"><span
                    class="form-check-label">외부</span></label> <label class="form-check form-check-inline">
                  <input type="checkbox" class="form-check-input" id="footfall[0][none]"><span
                    class="form-check-label">미설정</span></label> </td>
            </tr>
            <tr>
              <td>Bar Graph B</td>
              <td><select class="form-control" id="footfall[1][title]">
                  <option value="lastweek">lastweek</option>
                  <option value="thisweek" selected>thisweek</option>
                </select></td>
              <td><input type="text" id="footfall[1][display]" class="form-control" value="이번주"></td>
              <td><label class="form-check form-check-inline">
                  <input type="checkbox" class="form-check-input" id="footfall[1][entrance]" checked><span
                    class="form-check-label">입구</span></label> <label class="form-check form-check-inline">
                  <input type="checkbox" class="form-check-input" id="footfall[1][exit]"><span
                    class="form-check-label">출구</span></label> <label class="form-check form-check-inline">
                  <input type="checkbox" class="form-check-input" id="footfall[1][outside]"><span
                    class="form-check-label">외부</span></label> <label class="form-check form-check-inline">
                  <input type="checkbox" class="form-check-input" id="footfall[1][none]"><span
                    class="form-check-label">미설정</span></label> </td>
            </tr>
            <tr>
              <td>Curve Chart A</td>
              <td><input type="text" class="form-control" id="footfall[2][title]" value="last12weeks" readonly></td>
              <td><input type="text" id="footfall[2][display]" class="form-control" value="12주 유동량"></td>
              <td><label class="form-check form-check-inline">
                  <input type="checkbox" class="form-check-input" id="footfall[2][entrance]" checked><span
                    class="form-check-label">입구</span></label> <label class="form-check form-check-inline">
                  <input type="checkbox" class="form-check-input" id="footfall[2][exit]"><span
                    class="form-check-label">출구</span></label> <label class="form-check form-check-inline">
                  <input type="checkbox" class="form-check-input" id="footfall[2][outside]"><span
                    class="form-check-label">외부</span></label> <label class="form-check form-check-inline">
                  <input type="checkbox" class="form-check-input" id="footfall[2][none]"><span
                    class="form-check-label">미설정</span></label> </td>
            </tr>
            <tr>
              <td>Curve Chart B</td>
              <td><input type="text" class="form-control" id="footfall[3][title]" value="last12weeks" readonly></td>
              <td><input type="text" id="footfall[3][display]" class="form-control" value=""></td>
              <td><label class="form-check form-check-inline">
                  <input type="checkbox" class="form-check-input" id="footfall[3][entrance]"><span
                    class="form-check-label">입구</span></label> <label class="form-check form-check-inline">
                  <input type="checkbox" class="form-check-input" id="footfall[3][exit]"><span
                    class="form-check-label">출구</span></label> <label class="form-check form-check-inline">
                  <input type="checkbox" class="form-check-input" id="footfall[3][outside]"><span
                    class="form-check-label">외부</span></label> <label class="form-check form-check-inline">
                  <input type="checkbox" class="form-check-input" id="footfall[3][none]"><span
                    class="form-check-label">미설정</span></label> </td>
            </tr>
          </table>
          <button type="button" name="footfall" class="btn btn-primary" value="footfall"
            OnClick="changeOption(this)">저장</button>
          <span id="footfall_result"></span>
        </div>
      </div>
      <div class="card">
        <div class="card-header">
          <h5 class="card-title mb-0">Thrid Block Section</h5>
        </div>
        <div class="card-body">
          <div class="form-row form-group">
            <div class="col-md-4">
              <label>Category</label>
              <select class="form-control" id="third_block" onchange="third_display()">
                <option value="none">없슴</option>
                <option value="age_gender">성별 / 연령</option>
                <option value="curve_by_label" selected>레이블별 통계</option>
                <option value="tablefor">표</option>
              </select>
            </div>
            <div class="col-md-8">
              <label>Dispaly</label>
              <input type="text" id="third_block_display" class="form-control" value="third_block_display">
            </div>
          </div>
          <table id="third_block_curve_block" style="display:none"
            class="table table-striped table-sm table-bordered table-hover">
            <tbody>
              <thead>
                <tr>
                  <th></th>
                  <th>표시</th>
                  <th>카운터 라벨</th>
                </tr>
              </thead>
              <tr>
                <td>0</td>
                <td><input type="text" id="curve_label[0][display]" class="form-control"
                    value="curve_by_label0_display"></td>
                <td><label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[0][entrance]" checked><span
                      class="form-check-label">입구</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[0][exit]"><span
                      class="form-check-label">출구</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[0][outside]"><span
                      class="form-check-label">외부</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[0][none]"><span
                      class="form-check-label">미설정</span></label> </td>
                <td><input type="color" id="curve_label[0][color]" class="form-control" value="#47bac1"></td>
              </tr>
              <tr>
                <td>1</td>
                <td><input type="text" id="curve_label[1][display]" class="form-control"
                    value="curve_by_label1_display"></td>
                <td><label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[1][entrance]"><span
                      class="form-check-label">입구</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[1][exit]" checked><span
                      class="form-check-label">출구</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[1][outside]"><span
                      class="form-check-label">외부</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[1][none]"><span
                      class="form-check-label">미설정</span></label> </td>
                <td><input type="color" id="curve_label[1][color]" class="form-control" value="#fcc100"></td>
              </tr>
              <tr>
                <td>2</td>
                <td><input type="text" id="curve_label[2][display]" class="form-control"
                    value="curve_by_label2_display"></td>
                <td><label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[2][entrance]"><span
                      class="form-check-label">입구</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[2][exit]"><span
                      class="form-check-label">출구</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[2][outside]"><span
                      class="form-check-label">외부</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[2][none]"><span
                      class="form-check-label">미설정</span></label> </td>
                <td><input type="color" id="curve_label[2][color]" class="form-control" value="#5b7dff"></td>
              </tr>
              <tr>
                <td>3</td>
                <td><input type="text" id="curve_label[3][display]" class="form-control"
                    value="curve_by_label3_display"></td>
                <td><label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[3][entrance]"><span
                      class="form-check-label">입구</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[3][exit]"><span
                      class="form-check-label">출구</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[3][outside]"><span
                      class="form-check-label">외부</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[3][none]"><span
                      class="form-check-label">미설정</span></label> </td>
                <td><input type="color" id="curve_label[3][color]" class="form-control" value="#5fc27e"></td>
              </tr>
              <tr>
                <td>4</td>
                <td><input type="text" id="curve_label[4][display]" class="form-control"
                    value="curve_by_label4_display"></td>
                <td><label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[4][entrance]"><span
                      class="form-check-label">입구</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[4][exit]"><span
                      class="form-check-label">출구</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[4][outside]"><span
                      class="form-check-label">외부</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[4][none]"><span
                      class="form-check-label">미설정</span></label> </td>
                <td><input type="color" id="curve_label[4][color]" class="form-control" value="#50c27e"></td>
              </tr>
              <tr>
                <td>5</td>
                <td><input type="text" id="curve_label[5][display]" class="form-control"
                    value="curve_by_label5_display"></td>
                <td><label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[5][entrance]"><span
                      class="form-check-label">입구</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[5][exit]"><span
                      class="form-check-label">출구</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[5][outside]"><span
                      class="form-check-label">외부</span></label> <label class="form-check form-check-inline">
                    <input type="checkbox" class="form-check-input" id="curve_label[5][none]"><span
                      class="form-check-label">미설정</span></label> </td>
                <td><input type="color" id="curve_label[5][color]" class="form-control" value="#5f027e"></td>
              </tr>
            </tbody>
          </table>
          <table id="third_block_table_block" style="display:none"
            class="table table-striped table-sm table-bordered table-hover">
            <tbody></tbody>
          </table>
          <button type="button" name="third_block" class="btn btn-primary" value="third_block"
            OnClick="changeOption(this)">저장</button>
          <span id="third_block_result"></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup></script>

<style></style>