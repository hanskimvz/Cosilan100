<template>

<div class="row">
    <div class="col-md-6">
      <div class="card">
        <div class="card-header"><h5 class="card-title mb-0">程序</h5></div>
          <div class="card-body">
            <table class="table table-striped table-sm">
              <tr>
                <th>计数</th>
                <td><input type="checkbox" name="counting" value="yes" ></td>
                <td class="form-inline">托管服务 端口<input class="form-control ml-2" type="text" name="tlss_port" value="5000"></td>
              </tr>
              <tr>
                <th>实时计数</th>
                <td><input class="mr-1" type="radio" name="count_event" value="no" >否</td>
                <td class="form-inline"><input class="mr-1" type="radio" name="count_event" value="HTTP" >HTTP
                  <input class="ml-4 mr-1" type="radio" name="count_event" value="TCP" >TCP
                  <span class="ml-4 mt-1">端口 <input class="form-control ml-2" type="text" name="count_event_port" value=""></span>
                </td>
              </tr>
              <tr>
                <th>人脸检测</th>
                <td><input type="checkbox" name="face" value="yes" ></td>
                <td class="form-inline">端口<input class="form-control ml-2" type="text" name="face_port" value=""></td>
              </tr>
              <tr>
                <th>抓拍</th>
                <td><input type="checkbox" name="snapshot" value="yes" ></td>
                <td class="form-inline">端口<input class="form-control ml-2" type="text" name="snapshot_port" value="5020"></td>
              </tr>
              <tr>
                <th>手机探针</th>
                <td><input type="checkbox" name="macsniff" value="yes" ></td>
                <td class="form-inline">端口<input class="form-control ml-2" type="text" name="macsniff_port" value=""></td>
              </tr>
              <tr>
                <th>自动备份数据</th>
                <td><input type="checkbox" name="autobackup" value="yes" ></td>
                <td class="form-inline">间隔时间<input class="form-control ml-2 mr-1" type="text" name="autobackup_interval" value="1">day(s)</td>
              </tr>
              <tr>
                <th>自动升级</th>
                <td><input type="checkbox" name="autoupdate" value="yes" checked></td>
                <td class="form-inline"></td>
              </tr>
            </table>
          </div>
        </div>
      </div>
    </div>
    <div class="col-md-6">
      <div class="card">
        <div class="card-header"><h5 class="card-title mb-0">外部程序</h5></div>
        <div class="card-body">
          <table class="table table-striped table-sm">
            <tr>
              <th rowspan="4">旷视</th>
              <td>服务器</td>
              <td><input class="form-control" type="text" name="fpp_api_host" value="api-cn.faceplusplus.com"></td>
            </tr>
            <tr>
              <td>端口</td>
              <td><input class="form-control" type="text" name="fpp_api_port" value="443"></td>
            </tr>
            <tr>
              <td>API KEY</td>
              <td><input class="form-control" type="text" name="fpp_api_key" value="0OJg7382FP5t0R7F_CX5uXAAYcsdi6OT"></td>
            </tr>
            <tr>
              <td>API SRCT</td>
              <td><input class="form-control" type="text" name="fpp_api_srct" value="PZ4rrWY3LIfnb9TPCmLQvQWM8cmdrj14"></td>
            </tr>
            <tr>
              <th rowspan="4">天气</th>
              <td>服务器</td>
              <td><input class="form-control" type="text" name="weather_api_host" value="tianqiapi.com"></td>
            </tr>
            <tr>
              <td>端口</td>
              <td><input class="form-control" type="text" name="weather_api_port" value="443"></td>
            </tr>
            <tr>
              <td>API KEY</td>
              <td><input class="form-control" type="text" name="weather_api_key" value=""></td>
            </tr>
            <tr>
              <td>API SRCT</td>
              <td><input class="form-control" type="text" name="weather_api_srct" value=""></td>
            </tr>
          </table>
        </div>
      </div>
    </div>

</template>