import bpy
import os
import re
import time

regionsTopDir = 'K:/USAofPlasticv1/release_250m_v1/'

excludeList = []

def importSTL(abbr, printType, style):
  bpy.ops.import_mesh.stl(filepath=f'K:/USAofPlasticv1/release_250m_v1/{abbr}/{abbr}-{printType}{"-land-elevation" if printType == "dual" else ""}{"-" if len(style) > 0 else ""}{style}.STL')

  # import second model if dual PrintType
  if printType == "dual":
    bpy.ops.import_mesh.stl(filepath=f'K:/USAofPlasticv1/release_250m_v1/{abbr}/{abbr}-{printType}{"-hydrography" if printType == "dual" else ""}{"-" if len(style) > 0 else ""}{style}.STL')

def export3MF(abbr, printType, style, partNum):
  bpy.ops.object.select_all(action='DESELECT')

  for o in bpy.data.objects:
    # Check for given object names
    if re.search(f'{abbr}-{printType}{"-(?:land-elevation|hydrography)" if printType == "dual" else ""}{"-" if len(style) > 0 else ""}{style}{f"-p{partNum}" if partNum > 0 else ""}', o.name) is not None:
      o.select_set(True)

  # export objects
  if len(bpy.context.selected_objects) > 0:
    bpy.ops.export_mesh.threemf(filepath=f'K:/USAofPlasticv1/release_250m_v1/{abbr}/{abbr}-{printType}{"-" if len(style) > 0 else ""}{style}{f"-p{partNum}" if partNum > 0 else ""}.3mf', use_selection=True)

class ModalTimerOperator(bpy.types.Operator):
  """Operator which runs its self from a timer"""
  bl_idname = "wm.modal_timer_operator"
  bl_label = "Modal Timer Operator"

  _regionProcessStartTime = 0
  _regionList = []
  _regionPos = 0
  _variant = 0
  _timer = None

  def modal(self, context, event):
    #self.report({'INFO'}, f'{self._regionPos} {self._variant} {len(self._regionList)}')
    if event.type in {'ESC'} or self._regionPos == len(self._regionList):
        self.report({'INFO'}, f'finished {self._regionPos} {len(self._regionList)}')
        self._regionPos = 0
        self.cancel(context)
        return {'FINISHED'}

    rAbbr = self._regionList[self._regionPos]

    # Skip if region is in exclude list
    if rAbbr in excludeList:
        self.report({'INFO'}, f'Skipping {rAbbr} variant {self._variant}')
        self._regionPos += 1
        return {'PASS_THROUGH'}

    self.report({'INFO'}, f'Starting {rAbbr} variant {self._variant}')
    variantProcessStartTime = time.monotonic()

    if self._variant == 0:
        self._regionProcessStartTime = time.monotonic()
        # Import and export the different generated models
        importSTL(rAbbr, 'single', '')
        export3MF(rAbbr, 'single', '', 0)
        bpy.ops.object.delete() # delete the object afterwards to reduce unused memory usage
    elif self._variant == 1:
        importSTL(rAbbr, 'dual', '')
        export3MF(rAbbr, 'dual', '', 0)
        bpy.ops.object.delete()
    elif self._variant == 2:
        importSTL(rAbbr, 'dual', 'transparent')
        export3MF(rAbbr, 'dual', 'transparent', 0)
        bpy.ops.object.delete()
    elif self._variant == 3:
        # Export cut models (optional)
        export3MF(rAbbr, 'dual', 'transparent', 1)
        export3MF(rAbbr, 'dual', 'transparent', 2)
        export3MF(rAbbr, 'dual', 'transparent', 3)
        export3MF(rAbbr, 'dual', 'transparent', 4)
        self._regionPos += 1
    
    self.report({'INFO'}, f'{rAbbr} variant {self._variant} took {time.monotonic()-variantProcessStartTime}s')

    self._variant += 1
    if self._variant == 4:
       self.report({'INFO'}, f'{rAbbr} total time {time.monotonic()-self._regionProcessStartTime}s')
       self._variant = 0

    return {'PASS_THROUGH'}

  def execute(self, context):
    self._regionList = os.listdir(regionsTopDir)

    def get_dir_size(path='.', exclude3MF=True):
      total = 0
      with os.scandir(path) as it:
          for entry in it:
              if entry.is_file():
                  if entry.name.endswith('.stl'):
                      total += entry.stat().st_size
                  if exclude3MF and entry.name.endswith('transparent.3mf'):
                      excludeList.append(path[path.rfind('/')+1:])
              elif entry.is_dir():
                  total += get_dir_size(entry.path)
      return total

    self._regionList.sort(key=lambda f: get_dir_size(regionsTopDir+f), reverse=False)
    excludeList.sort(key=lambda f: get_dir_size(regionsTopDir+f, False), reverse=False)

    #self._regionList = ['TX']

    wm = context.window_manager
    self._timer = wm.event_timer_add(time_step=0.1, window=context.window)
    wm.modal_handler_add(self)
    return {'RUNNING_MODAL'}

  def cancel(self, context):
    wm = context.window_manager
    wm.event_timer_remove(self._timer)


def register():
    bpy.utils.register_class(ModalTimerOperator)


def unregister():
    bpy.utils.unregister_class(ModalTimerOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.wm.modal_timer_operator()
