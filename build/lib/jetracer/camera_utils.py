from jetcam.csi_camera import CSICamera

from jetcam.csi_camera import CSICamera
import cv2
import time

class JetRacerCamera:
    """wroking sets"""
    
    def __init__(self, mode='inference'):
        
        from jetcam.csi_camera import CSICamera
        
        if mode == 'inference':
            self.camera = CSICamera(width=640, height=480, capture_fps=21)
            self.target_size = (224, 224)
            self.mode = 'inference'
        elif mode == 'training':
            self.camera = CSICamera(width=640, height=480, capture_fps=21)
            self.target_size = (224, 224) 
            self.mode = 'training'
        elif mode == 'safe':
            self.camera = CSICamera(width=640, height=480, capture_fps=21)
            self.target_size = None 
            self.mode = 'safe'
        else:
            self.camera = CSICamera(width=640, height=480, capture_fps=21)
            self.target_size = (224, 224)
            self.mode = 'default'
        
        self._running = False
        print(f"created in '{mode}' mode")
        if self.target_size:
            print(f"resizingm 640x480 to {self.target_size[0]}x{self.target_size[1]}")
    
    def start(self):
        try:            
            if self._running:
                self.stop()
                time.sleep(1)
            
            self.camera.running = True
            self._running = True
            time.sleep(3)
            
            test_image = self.camera.value
            if test_image is not None:
                print(f"started")
                print(f"shape:  {test_image.shape}")
                
                processed = self._process_image(test_image)
                if processed is not None:
                    print(f"image shape after procesing: {processed.shape}")
                    return True
                else:
                    print("failed")
                    return False
            else:
                return False
                
        except Exception as e:
            print(f"failed: {e}")
            return False
    
    def stop(self):
        try:
            if hasattr(self, 'camera') and self.camera:
                self.camera.running = False
                self._running = False
                time.sleep(1)
                print("stopped")
        except Exception as e:
    
    def _process_image(self, image):
        if image is None:
            return None
        
        if self.target_size:
            try:
                resized = cv2.resize(image, self.target_size)
                return resized
            except Exception as e:
                print(f"failed resizeing {e}")
                return image
        
        return image
    
    def read(self):
        try:
            if not self._running:
                print("cam off")
                return None
            
            raw_image = self.camera.value
            return self._process_image(raw_image)
            
        except Exception as e:
            print(f"Error reading from camera: {e}")
            return None
    
    @property
    def value(self):
        return self.read()
    
    @property
    def raw_value(self):
        if hasattr(self.camera, 'value'):
            return self.camera.value
        return None
    
    @property
    def running(self):
        return self._running
    
    @property
    def width(self):
        return self.target_size[0] if self.target_size else 640
    
    @property
    def height(self):
        return self.target_size[1] if self.target_size else 480
    
    def observe(self, callback, names='value'):
        if hasattr(self.camera, 'observe'):
            def wrapped_callback(change):
                if 'new' in change:
                    processed = self._process_image(change['new'])
                    new_change = change.copy()
                    new_change['new'] = processed
                    callback(new_change)
                else:
                    callback(change)
            
            return self.camera.observe(wrapped_callback, names=names)
        return None
    
    def unobserve_all(self):
        """Unobserve all callbacks"""
        if hasattr(self.camera, 'unobserve_all'):
            return self.camera.unobserve_all()

def test_jetracer_camera():
    modes = ['safe', 'training', 'inference']
    
    for mode in modes:
        print(f"\n{'='*20} Testing {mode} mode {'='*20}")
        try:
            cam = JetRacerCamera(mode)
            if cam.start():
                for i in range(3):
                    img = cam.read()
                    if img is not None:
                    else:
                    time.sleep(0.5)
                cam.stop()
            else:
            time.sleep(2)
        except Exception as e:
            print(f"✗ {mode} mode error: {e}")


import gc
import time

def release_all_cameras():
    
    import inspect
    frame = inspect.currentframe().f_back
    caller_globals = frame.f_globals
    
    camera_vars = []
    for var_name in list(caller_globals.keys()):
        try:
            obj = caller_globals[var_name]
            if (hasattr(obj, 'running') or 
                hasattr(obj, 'cap') or 
                'camera' in str(type(obj)).lower() or
                'CSI' in str(type(obj))):
                camera_vars.append(var_name)
        except:
            pass
    
    
    for var_name in camera_vars:
        try:
            obj = caller_globals[var_name]
            if hasattr(obj, 'running'):
                obj.running = False
            if hasattr(obj, 'stop'):
                obj.stop()
            if hasattr(obj, 'cap') and hasattr(obj.cap, 'release'):
                obj.cap.release()
            del caller_globals[var_name]
        except Exception as e:
            print(f"cleaning error {var_name}: {e}")
    
    gc.collect()
    
    time.sleep(3)
    
    print("released")

def quick_camera_test():
    try:
        from jetcam.csi_camera import CSICamera
        test_cam = CSICamera(width=640, height=480, capture_fps=21)
        test_cam.running = True
        time.sleep(2)
        
        img = test_cam.value
        if img is not None:
            result = True
        else:
            result = False
            
        test_cam.running = False
        del test_cam
        return result
        
    except Exception as e:
        return False

def safe_camera_create(camera_class, *args, **kwargs):
    
    release_all_cameras()
    
    try:
        camera = camera_class(*args, **kwargs)
        return camera
    except Exception as e:
        return None

def release_cam():
    release_all_cameras()

def test_cam():
    return quick_camera_test()

