var configList = [];
var pageSizeList = [
  {
    name: "A0",
    width: "841",
    height: "1189"
  }, {
    name: "A1",
    width: "594",
    height: "841"
  }, {
    name: "A2",
    width: "420",
    height: "594"
  }, {
    name: "A3",
    width: "297",
    height: "420"
  }, {
    name: "A4",
    width: "210",
    height: "297"
  }, {
    name: "A5",
    width: "148",
    height: "210"
  }, {
    name: "A6",
    width: "105",
    height: "148"
  }, {
    name: "A7",
    width: "74",
    height: "105"
  }, {
    name: "A8",
    width: "52",
    height: "74"
  }, {
    name: "A9",
    width: "37",
    height: "52"
  }, {
    name: "A10",
    width: "26",
    height: "37"
  }, {
    name: "B0",
    width: "1000",
    height: "1414"
  }, {
    name: "B1",
    width: "707",
    height: "1000"
  }, {
    name: "B2",
    width: "500",
    height: "707"
  }, {
    name: "B3",
    width: "353",
    height: "500"
  }, {
    name: "B4",
    width: "250",
    height: "353"
  }, {
    name: "B5",
    width: "176",
    height: "250"
  }, {
    name: "B6",
    width: "125",
    height: "176"
  }, {
    name: "B7",
    width: "88",
    height: "125"
  }, {
    name: "B8",
    width: "62",
    height: "88"
  }, {
    name: "B9",
    width: "44",
    height: "62"
  }, {
    name: "B10",
    width: "31",
    height: "44"
  }
];

function log(data) {
  console.log(data);
}

// function configSelectChange() {
//   reset();
//   // if (configList.length) {
//   //   code = $("#template-code-modify").val();
//   //   configList.map(function(current) {
//   //     if (current.temple_code === code) {
//   //       setConfig(current)
//   //     }
//   //   })
//   // }
// }

$(document).ready(function() {

  /*** 电子称 ***/

  function getPortList() {
    $.ajax({
      type: "GET",
      url: "port",
      dataType: "text",
      success: function(dataMap) {
        var fieldList = dataMap.split("&");
        for (var i = 0; i < fieldList.length; i++) {
          $("<option value='" + fieldList[i] + "'>" + fieldList[i] + "</option>").appendTo(".port");
        }
      }
    });
  }

  function getCurrentConfig() {
    $.ajax({
      type: "GET",
      url: "get/config",
      dataType: "text",
      success: function(dataMap) {
        dataMap = dataMap.substring(1, dataMap.length - 1);
        dataMap = dataMap.replace(/'/g, '"');
        dataMap = JSON.parse(dataMap);
        $(".result-port").text(dataMap.port);
        $(".result-rate").text(dataMap.rate);
        $(".result-timeout").text(dataMap.timeout);
      }
    });
  }

  function bindScaleTestingEvent() {
    $(".test").click(function() {
      data = {
        port: $(".port").val(),
        rate: $(".rate").val(),
        timeout: $(".timeout").val()
      }
      $.ajax({
        type: "POST",
        url: "test",
        data: data,
        dataType: "text",
        success: function(result) {
          alert(result);
        }
      });
    });
  }

  function bindScaleModifyEvent() {
    $(".read-btn").click(function() {
      $.ajax({
        type: "GET",
        url: "original/data",
        dataType: "text",
        success: function(result) {
          $(".result").text(result);
        }
      });
    });
  }



  /*** 打印机 ***/

  function bindTabEvent() {
    $(".nav-tabs .tab-item").click(function() {
      $(this).addClass("active").siblings().removeClass("active");
      $(".tab-content .tab-pane").eq($(this).index()).addClass("active in").siblings().removeClass("active in");
    })
  }

  function bindPrinterTestingEvent() {
    $("#printer-test").click(function() {
      data = {
        content: $("#print-content").val(),
        temple_code: $("#template-code-list").val()
      }
      $.ajax({
        type: "POST",
        url: "test/print",
        data: JSON.stringify(data),
        dataType: "text",
        contentType: "application/json; charset=utf-8",
        success: function(result) {
          alert(result);
        }
      });
    });
  }

  function isChecked(id) {
    return $("#" + id).prop("checked") === true;
  }

  function findConfigFromList(list, key, value) {
    if (!list.length) return;
    return list.find(function(item) {
      return item[key] === value;
    })
  }

  /*** 打印机列表 ***/
  function getPrinterList() {
    $.ajax({
      type: "GET",
      url: "printers",
      dataType: "text",
      success: function(data) {
        var printerList = JSON.parse(data);
        if (printerList.length) {
          printerList.map(function(current) {
            $("<option value='" + current + "'>" + current + "</option>").appendTo("#printer-name");
          });
        }
      }
    });
  }

  /*** 配置列表 ***/
  function getConfigList() {
    var configListTpl, templateCodeListTpl;
    $.ajax({
      type: "GET",
      url: "get/all/printer",
      dataType: "text",
      success: function(data) {
        configList = JSON.parse(data);
        if (configList.length) {
          configList.map(function(current, index) {
          configListTpl = "<tr class='config-list-item'><td class='template-code'>" + current.temple_code + "</td><td>" + current.printer_name + "</td><td>" + current.page_width + "*" + current.page_height +  "</td><td>" + current.margin_top + "</td><td>" + current.margin_bottom + "</td><td>" + current.margin_left + "</td><td>" + current.margin_right + "</td><td><span class='oper-modify'>编辑</span><span class='oper-delete'>删除</span></td></tr>";
          templateCodeListTpl = "<option value='" + current.temple_code + "'>" + current.temple_code + "</option>";
          $(configListTpl).appendTo("#config-list");
          $(templateCodeListTpl).appendTo("#template-code-list");
          })
        }
      }
    });
  }
  function removeConfigList() {
    if ($(".config-list-item").length > 0) {
      $(".config-list-item").each(function() {
        $(this).remove();
      });
    }
  }
  function updateConfigList() {
    removeConfigList();
    getConfigList();
  }

  function bindConfigListOperEvent() {
    $("#config-list").on("click", ".oper-modify", function(e) {
      var code = $(this).parent().siblings(".template-code").html();
      var config = findConfigFromList(configList, "temple_code", code);
      initOperModal("modify", config);
      $("#oper-modal").show();
    });

    $("#config-list").on("click", ".oper-delete", function(e) {
      var r = confirm("确认删除？");
      if (r === true) {
        var code = $(this).parent().siblings(".template-code").html();
        var data = {
          temple_code: code
        };
        $.ajax({
          type: "POST",
          url: "delete/temple",
          data: JSON.stringify(data),
          dataType: "text",
          contentType: "application/json; charset=utf-8",
          success: function(result) {
            alert(result);
            if (result === "success") {
              updateConfigList();
            }
          }
        });
      }
    });
  }



  /*** 弹框 ***/

  function initOperModal(label, data) {
    $("#modal-title-" + label).show().siblings().hide();
    $("#modal-btn-" + label).show().siblings().hide();
    if (label === "new") {
      $("#template-code-new").show();
      $("#template-code-modify").hide();
    } else {
      $("#template-code-modify").show();
      $("#template-code-new").hide();
      data && setConfig(data);
    }
  }
  function resetModal() {
    $("#template-code-new").val("");
    $("#printer-name").val("");
    $("#margin-top").val("");
    $("#margin-bottom").val("");
    $("#margin-left").val("");
    $("#margin-right").val("");
    if (isChecked("cus-ps-checkbox")) {
      resetCusPSCheckbox(false);
    } else {
      $("#page-size").val("");
    }
  }
  // 纸张尺寸下拉/输入切换
  function resetCusPSCheckbox(checked) {
    if (!checked) {
      $("#cus-ps-width").val("");
      $("#cus-ps-height").val("");
      $("#cus-ps-checkbox").prop("checked", false);
      $("#cus-ps-wrapper").css("display", "none");;
      $("#page-size").show();
    } else {
      $("#page-size").val("");
      $("#cus-ps-checkbox").prop("checked", true);
      $("#cus-ps-wrapper").css("display", "inline-block");
      $("#page-size").hide();
    }
  }
  // 获取纸张尺寸的值
  function getPageSize() {
    if (isChecked("cus-ps-checkbox")) {
      return {
        pageWidth: $("#cus-ps-width").val(),
        pageHeight: $("#cus-ps-height").val()
       }
    } else {
      if ($("#page-size").val()) {
        var arr = JSON.parse($("#page-size").val());
        return {
          pageWidth: arr[0],
          pageHeight: arr[1]
        }
      } else {
        return {
          pageWidth: null,
          pageHeight: null
        }
      }
    }
  }
  // 填充纸张尺寸
  function setPageSize(pageWidth, pageHeight) {
    if (findConfigFromList(pageSizeList, "width", pageWidth) && findConfigFromList(pageSizeList, "height", pageHeight)) {
      resetCusPSCheckbox(false);
      $("#page-size").val(JSON.stringify([pageWidth, pageHeight]));
    } else {
      resetCusPSCheckbox(true);
      $("#cus-ps-width").val(pageWidth);
      $("#cus-ps-height").val(pageHeight);
    }
  }
  function setConfig(data) {
    $("#template-code-modify").html(data.temple_code);
    $("#printer-name").val(data.printer_name);
    $("#margin-top").val(data.margin_top);
    $("#margin-bottom").val(data.margin_bottom);
    $("#margin-left").val(data.margin_left);
    $("#margin-right").val(data.margin_right);
    setPageSize(data.page_width, data.page_height);
  }
  function saveConfig(label) {
    var code = label === "new" ? $("#template-code-new").val() : $("#template-code-modify").html();
    var pageSize = getPageSize();
    var data = {
      // isdefault: $("#is-default-checkbox").is(":checked") + "",
      temple_code: code,
      printer_name: $("#printer-name").val(),
      page_width: pageSize.pageWidth,
      page_height: pageSize.pageHeight,
      margin_left: $("#margin-left").val(),
      margin_top: $("#margin-top").val(),
      margin_right: $("#margin-right").val(),
      margin_bottom: $("#margin-bottom").val()
    };
    $.ajax({
      type: "POST",
      url: "set/printer",
      data: JSON.stringify(data),
      contentType: "application/json; charset=utf-8",
      dataType: "text",
      success: function(result) {
        alert(result);
        if (result === "success") {
          $("#oper-modal").hide();
          resetModal();
          updateConfigList();
        }
      }
    });
  }

  // 绑定弹框显示隐藏事件
  function bindShowPrevModalEvent() {
    $("#pre-modal-btn").click(function() {
      $("#prev-modal").show();
      $("#prev-modal .content").html($("#print-content").val());
    });
  }
  function bindClosePrevModalEvent() {
    $("#prev-modal .close-label").click(function() {
      $("#prev-modal").hide();
    });
    $("#prev-modal").click(function(e) {
      e.stopPropagation();
      if (e.target.className === "cover") {
        $("#prev-modal").hide();
      }
    });
  }
  function bindShowOperModalEvent() {
    $("#oper-modal-btn").click(function() {
      initOperModal("new");
      $("#oper-modal").show();
    });
  }
  function bindCloseOperModalEvent() {
    $("#oper-modal .close-label").click(function() {
      $("#oper-modal").hide();
      resetModal();
    });
  }

  // 绑定新增/编辑配置事件
  function bindBtnNewEvent() {
    $("#modal-btn-new").click(function() {
      saveConfig("new");
    });
  }
  function bindBtnModifyEvent() {
    $("#modal-btn-modify").click(function() {
      saveConfig("modify");
    });
  }
  function bindShowCusPageSizeEvent() {
    $("#cus-ps-checkbox").click(function(e) {
      if (e.target.checked === true) {
        $("#page-size").val("");
        $("#cus-ps-wrapper").css("display", "inline-block");
        $("#page-size").hide();
      } else {
        $("#cus-ps-height").val("");
        $("#cus-ps-width").val("");
        $("#cus-ps-wrapper").css("display", "none");;
        $("#page-size").show();
      }
    })
  }


  function bindEvent() {
    bindTabEvent();
    bindScaleTestingEvent();
    bindScaleModifyEvent();
    bindPrinterTestingEvent();
    bindShowPrevModalEvent();
    bindClosePrevModalEvent();
    bindShowOperModalEvent();
    bindCloseOperModalEvent();
    bindBtnNewEvent();
    bindBtnModifyEvent();
    bindShowCusPageSizeEvent();
    bindConfigListOperEvent();
  }

  bindEvent();
  getPortList();
  getCurrentConfig();
  // 打印
  getConfigList();
  getPrinterList();
});
