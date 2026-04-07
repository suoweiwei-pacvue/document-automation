"""Tests for code parsers."""

from src.parsing.java_parser import parse_java_file
from src.parsing.vue_parser import parse_vue_file, parse_js_file
from src.parsing.markdown_parser import parse_confluence_page


SAMPLE_JAVA = '''
package com.pacvue.api.controller;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/customDashboard")
public class DashboardController {

    @GetMapping("/list")
    public Result<List<DashboardVO>> list(@RequestParam Long clientId) {
        return dashboardService.listByClientId(clientId);
    }

    @PostMapping("/queryChart")
    public Result<ChartDataVO> queryChart(@RequestBody QueryChartRequest request) {
        return chartHandler.handle(request);
    }
}
'''

SAMPLE_VUE = '''
<template>
  <div class="dashboard-container">
    <chart-list :charts="charts" @edit="onEdit" />
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return { charts: [] }
  },
  methods: {
    async onEdit(chartId) {
      const result = await this.$api.editChart(chartId);
      this.charts = result.data;
    }
  }
}
</script>

<style scoped>
.dashboard-container { padding: 20px; }
</style>
'''

SAMPLE_CONFLUENCE = '''## 交接文档

### 核心API

/customDashboard/queryChart 是最重要的接口。

### 数据流

ChartHandler -> SettingHandler -> CollectorHandler

### 数据库

dashboard 表和 chart 表是主要表结构。
'''


def test_java_parser_extracts_class():
    chunks = parse_java_file(SAMPLE_JAVA, "DashboardController.java")
    assert len(chunks) >= 1
    class_chunk = next((c for c in chunks if c.chunk_type == "class"), None)
    assert class_chunk is not None
    assert class_chunk.name == "DashboardController"
    assert class_chunk.package == "com.pacvue.api.controller"


def test_java_parser_extracts_methods():
    chunks = parse_java_file(SAMPLE_JAVA, "DashboardController.java")
    method_names = [c.name for c in chunks if c.chunk_type == "method"]
    assert "list" in method_names
    assert "queryChart" in method_names


def test_vue_parser_extracts_sections():
    chunks = parse_vue_file(SAMPLE_VUE, "Dashboard.vue")
    chunk_types = {c.chunk_type for c in chunks}
    assert "template" in chunk_types
    assert "script" in chunk_types


def test_js_parser():
    js_code = "export function fetchData(url) { return fetch(url).then(r => r.json()); }"
    chunks = parse_js_file(js_code, "api.js")
    assert len(chunks) >= 1


def test_markdown_parser_splits_by_headings():
    chunks = parse_confluence_page(
        SAMPLE_CONFLUENCE, page_title="交接文档", page_id="123",
    )
    assert len(chunks) >= 1
    assert any("queryChart" in c.content for c in chunks)


def test_java_metadata():
    chunks = parse_java_file(SAMPLE_JAVA, "DashboardController.java")
    for chunk in chunks:
        meta = chunk.metadata
        assert "chunk_type" in meta
        assert "name" in meta
        assert meta["language"] == "java"
