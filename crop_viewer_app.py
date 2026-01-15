import cv2
import numpy as np
import os
import json
from typing import List, Tuple, Optional
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math


def calculate_dynamic_crops(
    width: int,
    height: int,
    crop_size: int = 224,
    max_overlap_ratio: float = 0.5,
    min_overlap_ratio: float = 0.0
) -> List[Tuple[int, int]]:
    """
    根據圖片尺寸動態計算切塊位置，自動調整重疊
    
    原理：
    - 如果圖片尺寸能被 crop_size 整除，則不重疊（stride = crop_size）
    - 如果無法整除，根據與 crop_size 倍數的差距動態調整覆蓋率
      - 差距越大，覆蓋率越高
      - 差距越小，覆蓋率越低
      - 覆蓋率會被限制在 min_overlap_ratio 和 max_overlap_ratio 之間
    
    Args:
        width: 圖片寬度
        height: 圖片高度
        crop_size: 切塊尺寸（預設 224）
        max_overlap_ratio: 最大重疊比例（0-1之間），預設 0.5（50%）
        min_overlap_ratio: 最小重疊比例（0-1之間），預設 0.0（0%，不重疊）
        
    Returns:
        切塊位置列表 [(x, y), ...]
    """
    if width < crop_size or height < crop_size:
        raise ValueError(f"圖片尺寸 ({width}x{height}) 小於切塊尺寸 ({crop_size}x{crop_size})")
    
    crop_locations = []
    
    # 計算 X 方向的切塊
    if width <= crop_size:
        # 圖片寬度小於等於切塊大小，只有一個切塊
        x_positions = [0]
    elif width % crop_size == 0:
        # 能被整除，不重疊
        num_crops_x = width // crop_size
        x_positions = [i * crop_size for i in range(num_crops_x)]
    else:
        # 無法整除，根據與 224 倍數的差距動態調整覆蓋率
        remainder = width % crop_size  # 餘數（與 224 倍數的差距）
        
        # 計算需要的切塊數量（確保能覆蓋整個寬度）
        num_crops_x = width // crop_size + 1
        
        # 根據餘數計算覆蓋率
        # 餘數越大，需要的覆蓋率越高
        # 覆蓋率 = remainder / crop_size，但限制在 min_overlap_ratio 和 max_overlap_ratio 之間
        overlap_ratio = min(max(remainder / crop_size, min_overlap_ratio), max_overlap_ratio)
        
        # 計算均勻的步長，確保所有切片之間的間距一致
        # 步長 = (width - crop_size) / (num_crops_x - 1)
        # 這樣可以確保最後一個切片正好在 width - crop_size 位置
        if num_crops_x == 1:
            stride_x = 0
            x_positions = [0]
        else:
            # 計算理想步長（確保最後一個切片在 width - crop_size）
            ideal_stride = (width - crop_size) / (num_crops_x - 1)
            # 限制步長，確保覆蓋率在合理範圍內
            min_stride = crop_size * (1 - max_overlap_ratio)
            max_stride = crop_size * (1 - min_overlap_ratio)
            
            # 如果理想步長在範圍內，直接使用
            if min_stride <= ideal_stride <= max_stride:
                stride_x = ideal_stride
            else:
                # 如果不在範圍內，使用最接近的邊界值
                stride_x = max(min_stride, min(ideal_stride, max_stride))
            
            # 使用線性插值生成所有位置，確保間距一致
            # 從 0 到 width - crop_size 均勻分佈
            x_positions = []
            for i in range(num_crops_x):
                if num_crops_x == 1:
                    x = 0
                else:
                    # 線性插值：i / (num_crops_x - 1) * (width - crop_size)
                    x_float = (i / (num_crops_x - 1)) * (width - crop_size)
                    x = int(round(x_float))
                x_positions.append(x)
            
            # 確保第一個和最後一個位置正確
            x_positions[0] = 0
            x_positions[-1] = width - crop_size
    
    # 計算 Y 方向的切塊
    if height <= crop_size:
        # 圖片高度小於等於切塊大小，只有一個切塊
        y_positions = [0]
    elif height % crop_size == 0:
        # 能被整除，不重疊
        num_crops_y = height // crop_size
        y_positions = [i * crop_size for i in range(num_crops_y)]
    else:
        # 無法整除，根據與 224 倍數的差距動態調整覆蓋率
        remainder = height % crop_size  # 餘數（與 224 倍數的差距）
        
        # 計算需要的切塊數量（確保能覆蓋整個高度）
        num_crops_y = height // crop_size + 1
        
        # 根據餘數計算覆蓋率
        # 餘數越大，需要的覆蓋率越高
        # 覆蓋率 = remainder / crop_size，但限制在 min_overlap_ratio 和 max_overlap_ratio 之間
        overlap_ratio = min(max(remainder / crop_size, min_overlap_ratio), max_overlap_ratio)
        
        # 計算均勻的步長，確保所有切片之間的間距一致
        # 步長 = (height - crop_size) / (num_crops_y - 1)
        # 這樣可以確保最後一個切片正好在 height - crop_size 位置
        if num_crops_y == 1:
            stride_y = 0
            y_positions = [0]
        else:
            # 計算理想步長（確保最後一個切片在 height - crop_size）
            ideal_stride = (height - crop_size) / (num_crops_y - 1)
            # 限制步長，確保覆蓋率在合理範圍內
            min_stride = crop_size * (1 - max_overlap_ratio)
            max_stride = crop_size * (1 - min_overlap_ratio)
            
            # 如果理想步長在範圍內，直接使用
            if min_stride <= ideal_stride <= max_stride:
                stride_y = ideal_stride
            else:
                # 如果不在範圍內，使用最接近的邊界值
                stride_y = max(min_stride, min(ideal_stride, max_stride))
            
            # 使用線性插值生成所有位置，確保間距一致
            # 從 0 到 height - crop_size 均勻分佈
            y_positions = []
            for i in range(num_crops_y):
                if num_crops_y == 1:
                    y = 0
                else:
                    # 線性插值：i / (num_crops_y - 1) * (height - crop_size)
                    y_float = (i / (num_crops_y - 1)) * (height - crop_size)
                    y = int(round(y_float))
                y_positions.append(y)
            
            # 確保第一個和最後一個位置正確
            y_positions[0] = 0
            y_positions[-1] = height - crop_size
    
    # 生成所有切塊位置
    for y in y_positions:
        for x in x_positions:
            # 確保不超出邊界
            if x + crop_size <= width and y + crop_size <= height:
                crop_locations.append((x, y))
    
    # 去重並排序
    crop_locations = sorted(list(set(crop_locations)))
    
    return crop_locations


class CropViewerApp:
    """圖片切片查看器應用程式"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("圖片切片查看器")
        # 初始視窗大小，載入圖片後會自動調整
        self.root.geometry("1200x800")
        
        # 變數
        self.image_path = None
        self.image = None
        self.image_rgb = None
        self.crop_locations = []
        self.crop_size = 224
        self.crop_images = []  # 儲存所有切片的 PIL Image 物件
        
        # 顯示相關變數
        self.display_image = None  # 顯示用的圖片（PIL Image）
        self.photo = None  # PhotoImage 物件
        self.scale_x = 1.0  # X 方向縮放比例
        self.scale_y = 1.0  # Y 方向縮放比例
        self.original_width = 0  # 原圖寬度
        self.original_height = 0  # 原圖高度
        
        # 切片狀態追蹤：'none', 'red', 'green'
        self.crop_states = {}  # {idx: 'none'/'red'/'green'}
        
        # 創建主框架
        self.create_widgets()
    
    def create_widgets(self):
        """創建介面元件"""
        # 頂部工具列
        toolbar = tk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        # 開啟圖片按鈕
        open_btn = tk.Button(
            toolbar,
            text="開啟圖片",
            command=self.open_image,
            width=12
        )
        open_btn.pack(side=tk.LEFT, padx=5)
        
        # 切片尺寸設定
        tk.Label(toolbar, text="切片尺寸:").pack(side=tk.LEFT, padx=5)
        self.crop_size_var = tk.StringVar(value="224")
        crop_size_entry = tk.Entry(toolbar, textvariable=self.crop_size_var, width=8)
        crop_size_entry.pack(side=tk.LEFT, padx=2)
        
        # 重新切片按鈕
        recrop_btn = tk.Button(
            toolbar,
            text="重新切片",
            command=self.recalculate_crops,
            width=12
        )
        recrop_btn.pack(side=tk.LEFT, padx=5)
        
        # 保存標籤按鈕
        save_label_btn = tk.Button(
            toolbar,
            text="保存標籤",
            command=self.save_labels,
            width=12
        )
        save_label_btn.pack(side=tk.LEFT, padx=5)
        
        # 儲存切片按鈕
        save_crops_btn = tk.Button(
            toolbar,
            text="儲存切片",
            command=self.save_crops,
            width=12
        )
        save_crops_btn.pack(side=tk.LEFT, padx=5)
        
        # 分隔線
        separator = ttk.Separator(toolbar, orient=tk.VERTICAL)
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # 批量標記按鈕
        tk.Label(toolbar, text="批量標記:", font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        
        set_all_green_btn = tk.Button(
            toolbar,
            text="全選綠",
            command=lambda: self.set_all_crops_state('green'),
            width=7,
            bg='#90EE90'
        )
        set_all_green_btn.pack(side=tk.LEFT, padx=2)
        
        set_all_red_btn = tk.Button(
            toolbar,
            text="全選紅",
            command=lambda: self.set_all_crops_state('red'),
            width=7,
            bg='#FFB6C1'
        )
        set_all_red_btn.pack(side=tk.LEFT, padx=2)
        
        set_all_none_btn = tk.Button(
            toolbar,
            text="清除",
            command=lambda: self.set_all_crops_state('none'),
            width=5
        )
        set_all_none_btn.pack(side=tk.LEFT, padx=2)
        
        # 資訊標籤
        self.info_label = tk.Label(
            toolbar,
            text="請先開啟圖片，然後點擊圖片上的位置選擇切片",
            font=('Arial', 10)
        )
        self.info_label.pack(side=tk.LEFT, padx=20)
        
        # 主內容區域（使用 Canvas + Scrollbar 實現滾動）
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 創建 Canvas 和滾動條
        self.canvas = tk.Canvas(main_frame, bg='white', cursor="crosshair")
        v_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # 綁定點擊事件
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # 佈局
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def open_image(self):
        """開啟圖片檔案"""
        file_path = filedialog.askopenfilename(
            title="選擇圖片",
            filetypes=[
                ("圖片檔案", "*.jpg *.jpeg *.png *.bmp"),
                ("所有檔案", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.image_path = file_path
                self.image = cv2.imread(file_path)
                
                if self.image is None:
                    messagebox.showerror("錯誤", "無法讀取圖片檔案")
                    return
                
                # 轉換為 RGB
                self.image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
                
                # 儲存原始尺寸
                self.original_height, self.original_width = self.image.shape[:2]
                
                # 計算切片並顯示
                self.calculate_and_display_crops()
                
            except Exception as e:
                messagebox.showerror("錯誤", f"讀取圖片時發生錯誤: {str(e)}")
    
    def recalculate_crops(self):
        """重新計算切片"""
        if self.image is None:
            messagebox.showwarning("警告", "請先開啟圖片")
            return
        
        try:
            # 更新切片尺寸
            self.crop_size = int(self.crop_size_var.get())
            
            if self.crop_size < 1:
                raise ValueError("切片尺寸必須大於 0")
            
            self.calculate_and_display_crops()
            
        except ValueError as e:
            messagebox.showerror("錯誤", f"無效的尺寸設定: {str(e)}")
        except Exception as e:
            messagebox.showerror("錯誤", f"重新切片時發生錯誤: {str(e)}")
    
    def save_labels(self):
        """保存標籤為 JSON 文件"""
        if self.image_path is None or not self.crop_locations:
            messagebox.showwarning("警告", "請先開啟圖片並進行切片")
            return
        
        try:
            # 構建 JSON 數據結構
            label_data = {
                "image_path": self.image_path,
                "image_name": os.path.basename(self.image_path),
                "image_width": self.original_width,
                "image_height": self.original_height,
                "crop_size": self.crop_size,
                "crops": []
            }
            
            # 添加每個切片的資訊（記錄所有切片，包括 state 為 'none' 的）
            for idx, (x, y) in enumerate(self.crop_locations):
                state = self.crop_states.get(idx, 'none')
                crop_info = {
                    "index": idx,
                    "x": x,
                    "y": y,
                    "state": state
                }
                label_data["crops"].append(crop_info)
            
            # 生成 JSON 文件名（與圖片同名，但擴展名為 .json）
            image_dir = os.path.dirname(self.image_path)
            image_name = os.path.basename(self.image_path)
            image_base_name = os.path.splitext(image_name)[0]
            json_file_path = os.path.join(image_dir, f"{image_base_name}.json")
            
            # 保存 JSON 文件
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(label_data, f, indent=2, ensure_ascii=False)
            
            # 統計標記數量
            red_count = sum(1 for state in self.crop_states.values() if state == 'red')
            green_count = sum(1 for state in self.crop_states.values() if state == 'green')
            
            messagebox.showinfo(
                "保存成功",
                f"標籤已保存到:\n{json_file_path}\n\n"
                f"總切片數: {len(self.crop_locations)}\n"
                f"紅色標記: {red_count}\n"
                f"綠色標記: {green_count}"
            )
            
        except Exception as e:
            messagebox.showerror("錯誤", f"保存標籤時發生錯誤: {str(e)}")
    
    def save_crops(self):
        """儲存有顏色的切片到對應資料夾"""
        if self.image_path is None or not self.crop_locations:
            messagebox.showwarning("警告", "請先開啟圖片並進行切片")
            return
        
        try:
            # 檢查是否有 JSON 文件
            image_dir = os.path.dirname(self.image_path)
            image_name = os.path.basename(self.image_path)
            image_base_name = os.path.splitext(image_name)[0]
            json_file_path = os.path.join(image_dir, f"{image_base_name}.json")
            
            if not os.path.exists(json_file_path):
                messagebox.showwarning("警告", "請先保存標籤文件（JSON）")
                return
            
            # 讀取 JSON 文件獲取標記狀態
            with open(json_file_path, 'r', encoding='utf-8') as f:
                label_data = json.load(f)
            
            # 創建資料夾
            normal_folder = os.path.join(image_dir, "normal_crop")
            bacterial_folder = os.path.join(image_dir, "bacterial_crop")
            os.makedirs(normal_folder, exist_ok=True)
            os.makedirs(bacterial_folder, exist_ok=True)
            
            # 統計保存的切片數量
            normal_count = 0
            bacterial_count = 0
            
            # 遍歷所有切片
            for idx, (x, y) in enumerate(self.crop_locations):
                # 從 JSON 或當前狀態獲取標記
                state = None
                for crop_info in label_data.get("crops", []):
                    if crop_info.get("index") == idx:
                        state = crop_info.get("state")
                        break
                
                # 如果 JSON 中沒有，使用當前狀態
                if state is None:
                    state = self.crop_states.get(idx, 'none')
                
                # 只保存有顏色的切片
                if state == 'green':
                    # 保存到 normal_crop 資料夾
                    crop_filename = f"{image_base_name}_{x}_{y}.jpg"
                    crop_path = os.path.join(normal_folder, crop_filename)
                    
                    # 提取切片
                    crop = self.image[y:y + self.crop_size, x:x + self.crop_size].copy()
                    
                    # 確保切片尺寸正確
                    if crop.shape[0] != self.crop_size or crop.shape[1] != self.crop_size:
                        if crop.shape[0] < self.crop_size or crop.shape[1] < self.crop_size:
                            pad_h = max(0, self.crop_size - crop.shape[0])
                            pad_w = max(0, self.crop_size - crop.shape[1])
                            crop = cv2.copyMakeBorder(
                                crop, 0, pad_h, 0, pad_w,
                                cv2.BORDER_REPLICATE
                            )
                        else:
                            crop = crop[:self.crop_size, :self.crop_size]
                    
                    # 保存切片
                    cv2.imwrite(crop_path, crop)
                    normal_count += 1
                    
                elif state == 'red':
                    # 保存到 bacterial_crop 資料夾
                    crop_filename = f"{image_base_name}_{x}_{y}.jpg"
                    crop_path = os.path.join(bacterial_folder, crop_filename)
                    
                    # 提取切片
                    crop = self.image[y:y + self.crop_size, x:x + self.crop_size].copy()
                    
                    # 確保切片尺寸正確
                    if crop.shape[0] != self.crop_size or crop.shape[1] != self.crop_size:
                        if crop.shape[0] < self.crop_size or crop.shape[1] < self.crop_size:
                            pad_h = max(0, self.crop_size - crop.shape[0])
                            pad_w = max(0, self.crop_size - crop.shape[1])
                            crop = cv2.copyMakeBorder(
                                crop, 0, pad_h, 0, pad_w,
                                cv2.BORDER_REPLICATE
                            )
                        else:
                            crop = crop[:self.crop_size, :self.crop_size]
                    
                    # 保存切片
                    cv2.imwrite(crop_path, crop)
                    bacterial_count += 1
            
            # 顯示保存結果
            messagebox.showinfo(
                "保存成功",
                f"切片已保存完成！\n\n"
                f"綠色切片（normal_crop）: {normal_count} 個\n"
                f"紅色切片（bacterial_crop）: {bacterial_count} 個\n\n"
                f"保存位置:\n"
                f"  {normal_folder}\n"
                f"  {bacterial_folder}"
            )
            
        except Exception as e:
            messagebox.showerror("錯誤", f"儲存切片時發生錯誤: {str(e)}")
    
    def load_labels(self):
        """讀取 label 文件並恢復標記狀態"""
        if self.image_path is None:
            return
        
        try:
            # 生成 JSON 文件路徑
            image_dir = os.path.dirname(self.image_path)
            image_name = os.path.basename(self.image_path)
            image_base_name = os.path.splitext(image_name)[0]
            json_file_path = os.path.join(image_dir, f"{image_base_name}.json")
            
            # 檢查文件是否存在
            if not os.path.exists(json_file_path):
                return  # 沒有 label 文件，直接返回
            
            # 讀取 JSON 文件
            with open(json_file_path, 'r', encoding='utf-8') as f:
                label_data = json.load(f)
            
            # 驗證 JSON 文件中的圖片資訊是否匹配
            if label_data.get("image_width") != self.original_width or \
               label_data.get("image_height") != self.original_height or \
               label_data.get("crop_size") != self.crop_size:
                # 圖片尺寸或切片尺寸不匹配，不讀取標籤
                return
            
            # 恢復標記狀態
            for crop_info in label_data.get("crops", []):
                idx = crop_info.get("index")
                x = crop_info.get("x")
                y = crop_info.get("y")
                state = crop_info.get("state")
                
                # 驗證索引和座標是否匹配
                if idx < len(self.crop_locations):
                    expected_x, expected_y = self.crop_locations[idx]
                    if x == expected_x and y == expected_y and state in ['red', 'green']:
                        self.crop_states[idx] = state
            
        except json.JSONDecodeError:
            # JSON 格式錯誤，忽略
            pass
        except Exception as e:
            # 讀取錯誤，忽略（不影響正常使用）
            pass
    
    def set_all_crops_state(self, state: str):
        """批量設置所有切片的狀態"""
        if not self.crop_locations:
            messagebox.showwarning("警告", "請先開啟圖片並進行切片")
            return
        
        # 設置所有切片狀態
        for idx in range(len(self.crop_locations)):
            self.crop_states[idx] = state
        
        # 更新遮罩顯示
        self.update_overlays()
        
        # 更新資訊標籤
        red_count = sum(1 for s in self.crop_states.values() if s == 'red')
        green_count = sum(1 for s in self.crop_states.values() if s == 'green')
        
        state_name = {'green': '綠色', 'red': '紅色', 'none': '無'}.get(state, state)
        self.info_label.config(
            text=f"圖片: {os.path.basename(self.image_path)} | "
                 f"尺寸: {self.original_width}x{self.original_height} | "
                 f"切片數: {len(self.crop_locations)} | "
                 f"切片大小: {self.crop_size}x{self.crop_size} | "
                 f"已全部設為 {state_name} | 紅色 {red_count}, 綠色 {green_count}"
        )
    
    def calculate_and_display_crops(self):
        """計算切片並在圖片上顯示分隔線"""
        if self.image is None:
            return
        
        # 計算切片位置
        self.crop_locations = calculate_dynamic_crops(
            self.original_width, self.original_height, self.crop_size,
            max_overlap_ratio=0.5,
            min_overlap_ratio=0.0
        )
        
        # 初始化所有切片的狀態為 'none'
        self.crop_states = {idx: 'none' for idx in range(len(self.crop_locations))}
        
        # 嘗試讀取 label 文件
        self.load_labels()
        
        # 統計標記數量
        red_count = sum(1 for state in self.crop_states.values() if state == 'red')
        green_count = sum(1 for state in self.crop_states.values() if state == 'green')
        label_info = ""
        if red_count > 0 or green_count > 0:
            label_info = f" | 已載入標籤: 紅色 {red_count}, 綠色 {green_count}"
        
        # 更新資訊標籤
        self.info_label.config(
            text=f"圖片: {os.path.basename(self.image_path)} | "
                 f"尺寸: {self.original_width}x{self.original_height} | "
                 f"切片數: {len(self.crop_locations)} | "
                 f"切片大小: {self.crop_size}x{self.crop_size}"
                 f"{label_info}"
        )
        
        # 生成所有切片（用於點擊後顯示）
        self.generate_crops()
        
        # 顯示圖片和分隔線
        self.display_image_with_grid()
    
    def generate_crops(self):
        """生成所有切片"""
        self.crop_images = []
        
        for idx, (x, y) in enumerate(self.crop_locations):
            # 提取切片
            crop = self.image_rgb[y:y + self.crop_size, x:x + self.crop_size].copy()
            
            # 確保切片尺寸正確
            if crop.shape[0] != self.crop_size or crop.shape[1] != self.crop_size:
                if crop.shape[0] < self.crop_size or crop.shape[1] < self.crop_size:
                    pad_h = max(0, self.crop_size - crop.shape[0])
                    pad_w = max(0, self.crop_size - crop.shape[1])
                    crop = np.pad(
                        crop,
                        ((0, pad_h), (0, pad_w), (0, 0)),
                        mode='edge'
                    )
                else:
                    crop = crop[:self.crop_size, :self.crop_size]
            
            # 轉換為 PIL Image
            crop_pil = Image.fromarray(crop)
            self.crop_images.append(crop_pil)
    
    def display_image_with_grid(self):
        """在 Canvas 上顯示圖片並畫分隔線"""
        if self.image_rgb is None:
            return
        
        # 清除 Canvas
        self.canvas.delete("all")
        
        # 獲取螢幕大小（考慮工具列和邊框）
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 預留空間給工具列、滾動條和邊框（約 150 像素）
        toolbar_height = 50
        scrollbar_width = 20
        padding = 20
        max_display_width = screen_width - scrollbar_width - padding * 2
        max_display_height = screen_height - toolbar_height - scrollbar_width - padding * 2
        
        # 計算顯示尺寸（限制在螢幕範圍內）
        if self.original_width > max_display_width or self.original_height > max_display_height:
            scale = min(max_display_width / self.original_width, max_display_height / self.original_height)
            display_width = int(self.original_width * scale)
            display_height = int(self.original_height * scale)
        else:
            display_width = self.original_width
            display_height = self.original_height
        
        # 計算縮放比例
        self.scale_x = display_width / self.original_width
        self.scale_y = display_height / self.original_height
        
        # 調整圖片大小
        self.display_image = Image.fromarray(self.image_rgb)
        if display_width != self.original_width or display_height != self.original_height:
            self.display_image = self.display_image.resize(
                (display_width, display_height),
                Image.Resampling.LANCZOS
            )
        
        # 轉換為 PhotoImage
        self.photo = ImageTk.PhotoImage(self.display_image)
        
        # 在 Canvas 上顯示圖片
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        
        # 設定 Canvas 的滾動區域
        self.canvas.configure(scrollregion=(0, 0, display_width, display_height))
        
        # 調整 Canvas 大小以適應圖片（但不超過顯示尺寸）
        self.canvas.config(width=min(display_width, max_display_width), 
                          height=min(display_height, max_display_height))
        
        # 調整視窗大小以適應內容
        # 計算視窗大小：工具列高度 + 圖片高度 + 滾動條 + 邊框
        window_width = min(display_width + scrollbar_width + padding * 2, screen_width)
        window_height = min(toolbar_height + display_height + scrollbar_width + padding * 2, screen_height)
        
        # 居中顯示視窗並設定大小
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 畫分隔線
        self.draw_grid_lines(display_width, display_height)
        
        # 畫遮罩
        self.draw_overlays(display_width, display_height)
    
    def draw_grid_lines(self, display_width: int, display_height: int):
        """在圖片上畫分隔線標示切片位置"""
        # 收集所有唯一的 x 和 y 位置
        x_positions = sorted(set(x for x, y in self.crop_locations))
        y_positions = sorted(set(y for x, y in self.crop_locations))
        
        # 畫垂直線（X 方向的分隔線）
        for x in x_positions:
            x_scaled = int(x * self.scale_x)
            self.canvas.create_line(
                x_scaled, 0,
                x_scaled, display_height,
                fill='yellow',
                width=2,
                tags="grid_line"
            )
            # 畫右邊界線
            x_right = int((x + self.crop_size) * self.scale_x)
            if x_right <= display_width:
                self.canvas.create_line(
                    x_right, 0,
                    x_right, display_height,
                    fill='yellow',
                    width=2,
                    tags="grid_line"
                )
        
        # 畫水平線（Y 方向的分隔線）
        for y in y_positions:
            y_scaled = int(y * self.scale_y)
            self.canvas.create_line(
                0, y_scaled,
                display_width, y_scaled,
                fill='yellow',
                width=2,
                tags="grid_line"
            )
            # 畫下邊界線
            y_bottom = int((y + self.crop_size) * self.scale_y)
            if y_bottom <= display_height:
                self.canvas.create_line(
                    0, y_bottom,
                    display_width, y_bottom,
                    fill='yellow',
                    width=2,
                    tags="grid_line"
                )
    
    def draw_overlays(self, display_width: int, display_height: int):
        """繪製切片遮罩"""
        # 刪除舊的遮罩
        self.canvas.delete("overlay")
        
        # 繪製每個切片的遮罩
        for idx, (x, y) in enumerate(self.crop_locations):
            state = self.crop_states.get(idx, 'none')
            if state != 'none':
                # 計算縮放後的座標
                x1 = int(x * self.scale_x)
                y1 = int(y * self.scale_y)
                x2 = int((x + self.crop_size) * self.scale_x)
                y2 = int((y + self.crop_size) * self.scale_y)
                
                # 根據狀態選擇顏色
                if state == 'red':
                    # 淺紅色遮罩（使用點狀圖案實現半透明效果）
                    fill_color = '#FFB6C1'  # LightPink
                    outline_color = '#FF69B4'  # HotPink（邊框稍深）
                else:  # green
                    # 淺綠色遮罩
                    fill_color = '#90EE90'  # LightGreen
                    outline_color = '#32CD32'  # LimeGreen（邊框稍深）
                
                # 繪製矩形遮罩（使用點狀圖案模擬半透明）
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=fill_color,
                    outline=outline_color,
                    width=2,
                    stipple='gray25',  # 使用點狀圖案實現半透明效果
                    tags="overlay"
                )
    
    def update_overlays(self):
        """更新遮罩顯示"""
        # 獲取當前顯示尺寸
        display_width = int(self.original_width * self.scale_x)
        display_height = int(self.original_height * self.scale_y)
        self.draw_overlays(display_width, display_height)
    
    def on_canvas_click(self, event):
        """處理 Canvas 點擊事件，根據點擊位置找到對應的切片"""
        if not self.crop_locations:
            return
        
        # 獲取 Canvas 上的點擊位置
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # 轉換為原圖座標
        original_x = int(canvas_x / self.scale_x)
        original_y = int(canvas_y / self.scale_y)
        
        # 找到包含該點的切片
        selected_idx = None
        for idx, (x, y) in enumerate(self.crop_locations):
            if (x <= original_x < x + self.crop_size and 
                y <= original_y < y + self.crop_size):
                selected_idx = idx
                break
        
        if selected_idx is not None:
            # 切換切片狀態：none -> red -> green -> none
            current_state = self.crop_states.get(selected_idx, 'none')
            if current_state == 'none':
                self.crop_states[selected_idx] = 'red'
            elif current_state == 'red':
                self.crop_states[selected_idx] = 'green'
            else:  # green
                self.crop_states[selected_idx] = 'none'
            
            # 更新遮罩顯示
            self.update_overlays()
        else:
            messagebox.showinfo("提示", f"點擊位置 ({original_x}, {original_y}) 不在任何切片範圍內")
    
    def on_crop_click(self, idx: int):
        """處理切片點擊事件，顯示切片詳情"""
        if idx < 0 or idx >= len(self.crop_locations):
            return
        
        x, y = self.crop_locations[idx]
        
        # 創建詳細資訊視窗
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"切片 #{idx + 1} 詳細資訊")
        detail_window.geometry("500x500")
        
        # 主框架
        main_frame = tk.Frame(detail_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 標題
        title_label = tk.Label(
            main_frame,
            text=f"切片 #{idx + 1}",
            font=('Arial', 14, 'bold')
        )
        title_label.pack(pady=10)
        
        # 顯示切片大圖
        if idx < len(self.crop_images):
            crop_pil = self.crop_images[idx]
            crop_large = crop_pil.resize((300, 300), Image.Resampling.LANCZOS)
            crop_photo_large = ImageTk.PhotoImage(crop_large)
            
            image_label = tk.Label(main_frame, image=crop_photo_large)
            image_label.image = crop_photo_large  # 保持引用
            image_label.pack(pady=10)
        
        # 資訊文字
        info_text = (
            f"切片編號: #{idx + 1}\n"
            f"位置: ({x}, {y})\n"
            f"切片尺寸: {self.crop_size}x{self.crop_size}\n"
            f"原圖尺寸: {self.original_width}x{self.original_height}\n"
            f"原圖路徑: {os.path.basename(self.image_path) if self.image_path else 'N/A'}\n"
            f"總切片數: {len(self.crop_locations)}"
        )
        
        info_label = tk.Label(
            main_frame,
            text=info_text,
            font=('Arial', 10),
            justify=tk.LEFT
        )
        info_label.pack(pady=10)
        
        # 關閉按鈕
        close_btn = tk.Button(
            main_frame,
            text="關閉",
            command=detail_window.destroy,
            width=15
        )
        close_btn.pack(pady=10)


def main():
    """主函數"""
    root = tk.Tk()
    app = CropViewerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

