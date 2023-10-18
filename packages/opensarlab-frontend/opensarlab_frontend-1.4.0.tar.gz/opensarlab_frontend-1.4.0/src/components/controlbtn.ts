import {
  JupyterFrontEnd
} from '@jupyterlab/application';

import { PartialJSONObject } from '@lumino/coreutils';

import { find } from '@lumino/algorithm';

import { 
  ToolbarButton
} from '@jupyterlab/apputils';

export function main( 
    app: JupyterFrontEnd,
    settings: PartialJSONObject
  ) {

    let enabled = settings.enabled as boolean;
    let rank = settings.rank as number;

    const widget_id = 'opensarlab-controlbtn'

    const widget = find(app.shell.widgets('top'), w => w.id === widget_id);
    if (widget) {
      widget.dispose()
    }  

    if(!enabled) {
      console.log('JupyterLab extension opensarlab-frontend:controlbtn is not activated!');
      return;
    }

    const serverBtn = new ToolbarButton({
      className: 'opensarlab-controlbtn',
      label: 'Shutdown and Logout Page',
      onClick: () => {
        window.location.href = '/hub/home';
      },
      tooltip: 'Hub Control Panel: A place to stop the server and logout'
    });
    serverBtn.id = widget_id;
    serverBtn.addClass('opensarlab-frontend-object');

    app.shell.add(serverBtn, 'top', {rank:rank});
    
    console.log('JupyterLab extension opensarlab-frontend:controlbtn is activated!');
  
  }
