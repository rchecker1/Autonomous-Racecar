# Updated camera_utils.py with PROVEN WORKING SETTINGS
# Replace your /home/checker/jetracer/jetracer/camera_utils.py with this content

from jetcam.csi_camera import CSICamera
import cv2
import time

class JetRacerCamera:
    """JetRacer camera with proven working configurations"""
    
    def __init__(self, mode='inference'):
        """
        Initialize camera for different use cases
        
        Args:
            mode: 'inference' for road following, 'training' for data collection, 'safe' for testing
        """
        # Based on our successful test: 640x480@21fps works perfectly
        # We'll scale to 224x224 in software if needed for models
        
        if mode == 'inference':
            # High performance for road following - use working config and resize
            self.camera = CSICamera(width=640, height=480, capture_fps=21)
            self.target_size = (224, 224)  # Resize for model input
            self.mode = 'inference'
        elif mode == 'training':
            # Same reliable config for training
            self.camera = CSICamera(width=640, height=480, capture_fps=21)
            self.target_size = (224, 224)  # Resize for model input
            self.mode = 'training'
        elif mode == 'safe':
            # Full resolution for testing/debugging
            self.camera = CSICamera(width=640, height=480, capture_fps=21)
            self.target_size = None  # No resizing
            self.mode = 'safe'
        else:
            # Default - same as safe
            self.camera = CSICamera(width=640, height=480, capture_fps=21)
            self.target_size = (224, 224)
            self.mode = 'default'
        
        self._running = False
        print(f"✓ JetRacer camera created in '{mode}' mode")
        if self.target_size:
            print(f"✓ Will resize from 640x480 to {self.target_size[0]}x{self.target_size[1]}")
    
    def start(self):
        """Start camera with proven working method"""
        try:
            print("Starting JetRacer camera...")
            
            # Stop if already running
            if self._running:
                self.stop()
                time.sleep(1)
            
            # Start camera using proven method
            self.camera.running = True
            self._running = True
            
            # Wait for initialization
            time.sleep(3)
            
            # Test capture using working method (.value)
            test_image = self.camera.value
            if test_image is not None:
                print(f"✓ Camera started successfully")
                print(f"✓ Raw image shape: {test_image.shape}")
                
                # Test processed image
                processed = self._process_image(test_image)
                if processed is not None:
                    print(f"✓ Processed image shape: {processed.shape}")
                    return True
                else:
                    print("✗ Image processing failed")
                    return False
            else:
                print("✗ Camera not capturing images")
                return False
                
        except Exception as e:
            print(f"✗ Camera start failed: {e}")
            return False
    
    def stop(self):
        """Stop camera safely"""
        try:
            if hasattr(self, 'camera') and self.camera:
                self.camera.running = False
                self._running = False
                time.sleep(1)
                print("✓ JetRacer camera stopped")
        except Exception as e:
            print(f"Warning during camera stop: {e}")
    
    def _process_image(self, image):
        """Process raw camera image"""
        if image is None:
            return None
        
        # If we need to resize for model input
        if self.target_size:
            try:
                resized = cv2.resize(image, self.target_size)
                return resized
            except Exception as e:
                print(f"Resize error: {e}")
                return image
        
        return image
    
    def read(self):
        """Read and process image from camera"""
        try:
            if not self._running:
                print("Warning: Camera not running")
                return None
            
            # Use proven working method
            raw_image = self.camera.value
            return self._process_image(raw_image)
            
        except Exception as e:
            print(f"Error reading from camera: {e}")
            return None
    
    @property
    def value(self):
        """Get current processed camera image"""
        return self.read()
    
    @property
    def raw_value(self):
        """Get current raw camera image (full resolution)"""
        if hasattr(self.camera, 'value'):
            return self.camera.value
        return None
    
    @property
    def running(self):
        """Check if camera is running"""
        return self._running
    
    @property
    def width(self):
        """Get output image width"""
        return self.target_size[0] if self.target_size else 640
    
    @property
    def height(self):
        """Get output image height"""
        return self.target_size[1] if self.target_size else 480
    
    def observe(self, callback, names='value'):
        """Observe camera changes (for compatibility with existing code)"""
        if hasattr(self.camera, 'observe'):
            # Create a wrapper to process images before callback
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

# Test function
def test_jetracer_camera():
    """Test all JetRacer camera modes"""
    modes = ['safe', 'training', 'inference']
    
    for mode in modes:
        print(f"\n{'='*20} Testing {mode} mode {'='*20}")
        try:
            cam = JetRacerCamera(mode)
            if cam.start():
                # Test multiple captures
                for i in range(3):
                    img = cam.read()
                    if img is not None:
                        print(f"✓ {mode} capture {i+1}: {img.shape}")
                    else:
                        print(f"✗ {mode} capture {i+1} failed")
                    time.sleep(0.5)
                cam.stop()
                print(f"✓ {mode} mode test complete")
            else:
                print(f"✗ {mode} mode failed to start")
            time.sleep(2)
        except Exception as e:
            print(f"✗ {mode} mode error: {e}")

# Usage:
# camera = JetRacerCamera('inference')  # For road following (224x224 output)
# camera = JetRacerCamera('training')   # For data collection (224x224 output)  
# camera = JetRacerCamera('safe')       # For testing (640x480 output)