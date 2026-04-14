<template>
  <div class="inspections-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>巡检任务</span>
          <el-button type="primary" @click="createInspection">创建巡检任务</el-button>
        </div>
      </template>
      
      <el-table :data="inspections" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="任务名称" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="viewInspection(row.id)">查看</el-button>
            <el-button size="small" type="danger" @click="deleteInspection(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 查看巡检结果 -->
    <el-dialog v-model="resultDialogVisible" title="巡检结果" width="80%">
      <div v-if="currentResult" class="inspection-result">
        <div class="result-header">
          <h3>{{ currentResult.name }}</h3>
          <p>执行时间：{{ currentResult.executed_at }}</p>
          <p>总主机数：{{ currentResult.total_hosts }}</p>
          <p>成功：{{ currentResult.success_count }}</p>
          <p>失败：{{ currentResult.failure_count }}</p>
        </div>
        
        <el-collapse v-model="activeNames">
          <el-collapse-item
            v-for="(value, key) in currentResult.results"
            :key="'key-' + key"
            :title="typeof key === 'number' ? 'Section ' + key : String(key)"
            :name="'item-' + key"
          >
            <div v-if="typeof value === 'object' && value !== null">
              <el-table :data="Array.isArray(value) ? value : [value]" style="width: 100%">
                <el-table-column v-for="(prop, index) in Object.keys(Array.isArray(value) ? value[0] : value)" :key="index" :prop="prop" :label="prop" />
              </el-table>
            </div>
            <div v-else>
              {{ value }}
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>
      <div v-else>
        加载中...
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      inspections: [],
      resultDialogVisible: false,
      currentResult: null,
      activeNames: []
    }
  },
  mounted() {
    this.getInspections()
  },
  methods: {
    async getInspections() {
      try {
        const response = await axios.get('/api/v1/inspections')
        this.inspections = response.data
      } catch (error) {
        this.$message.error('获取巡检任务失败')
      }
    },
    async createInspection() {
      try {
        const response = await axios.post('/api/v1/inspections', {
          name: `巡检任务_${new Date().toISOString()}`
        })
        this.$message.success('巡检任务创建成功')
        this.getInspections()
      } catch (error) {
        this.$message.error('创建巡检任务失败')
      }
    },
    async viewInspection(id) {
      try {
        const response = await axios.get(`/api/v1/inspections/${id}`)
        this.currentResult = response.data
        this.resultDialogVisible = true
      } catch (error) {
        this.$message.error('获取巡检结果失败')
      }
    },
    async deleteInspection(id) {
      try {
        await axios.delete(`/api/v1/inspections/${id}`)
        this.$message.success('巡检任务删除成功')
        this.getInspections()
      } catch (error) {
        this.$message.error('删除巡检任务失败')
      }
    },
    getStatusType(status) {
      const types = {
        'pending': 'info',
        'running': 'warning',
        'completed': 'success',
        'failed': 'danger'
      }
      return types[status] || 'info'
    },
    getStatusText(status) {
      const texts = {
        'pending': '待执行',
        'running': '执行中',
        'completed': '已完成',
        'failed': '失败'
      }
      return texts[status] || status
    }
  }
}
</script>

<style scoped>
.inspections-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.inspection-result {
  padding: 20px;
}

.result-header {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e4e7ed;
}

.result-header h3 {
  margin: 0 0 10px 0;
}

.result-header p {
  margin: 5px 0;
}
</style>