import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { PartialJSONObject } from '@lumino/coreutils';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { main as controlbtn } from './components/controlbtn';
import { main as doc_link } from './components/doc_link';
import { main as profile_label } from './components/profile_label'
import { main as oslnotify } from './components/oslnotify';
import { main as gifcap_btn } from './components/gifcap_btn';

/**
 * Initialization data for the opensarlab_frontend extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'opensarlab_frontend:plugin',
  description: 'A JupyterLab extension.',
  autoStart: true,
  optional: [ISettingRegistry],
  activate: (app: JupyterFrontEnd, settingRegistry: ISettingRegistry | null) => {
  
    function loadSetting(settings: ISettingRegistry.ISettings): void {

      gifcap_btn(app, settings.get('gifcap_btn').composite as PartialJSONObject);
      profile_label(app, settings.get('profile_label').composite as PartialJSONObject);
      doc_link(app, settings.get('doc_link').composite as PartialJSONObject);
      controlbtn(app, settings.get('controlbtn').composite as PartialJSONObject);
      oslnotify(app, settings.get('oslnotify').composite as PartialJSONObject);
    }

    // Wait for the application to be restored and
    // for the settings for this plugin to be loaded
    if(settingRegistry) {
      Promise.all([
            app.restored, 
            settingRegistry.load(plugin.id)
        ])
        .then(([, setting]) => {
          // Read the settings
          loadSetting(setting);

          // Listen for your plugin setting changes using Signal
          setting.changed.connect(loadSetting);
        });
    }

    console.log('JupyterLab extension opensarlab_frontend is fully operational!');
  }
};

export default plugin;
