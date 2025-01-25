<template>
  <div class="tree-container">
    <div class="node title">
        <h4 class="mb-0">{{ t('device_tree') }}</h4>
        <button class="toggle-btn" @click="toggleExpandedAll">{{ expandedAll ? '▼' : '▶' }}</button>
    </div>
    <ul class="tree">
        <li v-for="square in props.data" :key="square.code">
            <div class="node square">
                <span @click="handleClick(square, square.code, 0, 0)" :class="{'text-primary': square.code === 'new'}">{{ square.name }}</span>
                <button class="toggle-btn" @click="toggleChildren(square)">
                    {{ square.isExpanded ? '▼' : '▶' }}
                </button>
            </div>
            <ul v-if="square.store && square.isExpanded">
                <li v-for="store in square.store" :key="store.code">
                    <div class="node store">
                        <span @click="handleClick(0,square.code, store.code, 0)" :class="{'text-danger': store.code === 'new'}">{{ store.name }}</span>
                    </div>
                    <ul v-if="store.camera">
                        <li v-for="camera in store.camera" :key="camera.code">
                            <div class="node camera">
                                <span @click="handleClick(0, square.code, store.code, camera.code)" :class="{'text-warning': camera.code === 'new'}">{{ camera.name }}</span>
                            </div>
                        </li>
                    </ul>
                </li>
            </ul>
        </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const props = defineProps({
  data: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['click']);
const expandedAll = ref(false);

function handleClick(node, square_code, store_code, camera_code) {
    // console.log('handleClick', square_code, store_code, camera_code);
    if (node) {
        node.isExpanded = true;
    }
    emit('click', square_code, store_code, camera_code);
}

function toggleChildren(node) {
    node.isExpanded = !node.isExpanded;
}

const toggleExpandedAll = () => {
    expandedAll.value = !expandedAll.value;
    props.data.forEach(node => {
        node.isExpanded = expandedAll.value;
    });
}
</script>

<style scoped>
span {
  cursor: pointer;
}
.tree-container {
  padding: 20px;
}

.tree {
  list-style: none;
  padding-left: 20px;
}

.tree ul {
  list-style: none;
  padding-left: 30px;
  margin: 0;
}

.node {
  padding: 8px 15px;
  margin: 8px 0;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.tree li {
  position: relative;
  margin: 15px 0px;
  padding-left: 15px;
}

.tree li::before {
  content: "";
  position: absolute;
  left: 0;
  top: -15px;
  bottom: -15px;
  border-left: 1px solid #ccc;
}

.tree li::after {
  content: "";
  position: absolute;
  left: 0px;
  top: 18px;
  width: 15px;
  border-top: 1px solid #ccc;
}

.tree > li:first-child::before {
  top: 0;
}

.tree li:last-child::before {
  bottom: auto;
  height: 18px;
}

.tree ul > li:first-child::before {
  top: -15px;
}

.tree ul > li:last-child::before {
  bottom: auto;
  height: 33px;
}
.title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0;
  background-color: #94cffa;
}
.square {
  background-color: #e3f2fd;
  font-weight: bold;
}

.store {
  background-color: #f5f5f5;
}

.camera {
  background-color: #fff3e0;
}

.fas {
  width: 20px;
}

.toggle-btn {
  cursor: pointer;
  margin-left: auto;
  margin-right: 10px;
  font-size: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 2px 4px;
}
</style> 