import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the jupyterlab-ca-theme extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-ca-theme:plugin',
  description: 'A JupyterLab theme extension for Composable Analytics.',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log('JupyterLab extension jupyterlab-ca-theme is activated!');
    const style = 'jupyterlab-ca-theme/index.css';

    manager.register({
      name: 'jupyterlab-ca-theme',
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default plugin;
