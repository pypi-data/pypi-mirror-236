import React, { useCallback, useMemo, useState } from 'react';
import { styled } from 'styled-components';
import { ReactWidget } from '@jupyterlab/apputils';
import { Cell } from '@jupyterlab/cells';
import { Menu } from '@cognite/cogs.js';
import { Copilot } from '@cognite/copilot-core';
import useCogniteSDK from '../lib/hooks/useCogniteSDK';
import { track } from '../lib/track';
import { CodeGeneratorInputPanel } from './CodeGeneratorInputPanel';
import { CodeExplainerPanel } from './CodeExplainerPanel';

/**
 * A Lumino ReactWidget that wraps a CopilotMenu.
 */
export const CopilotWidget: React.FC<any> = ({
  activeCell
}: {
  activeCell: Cell;
}): any => {
  return ReactWidget.create(
    <div
      id="copilot_widget_root"
      style={{
        position: 'relative',
        zIndex: 100,
        height: '100vh',
        width: '100vw',
        pointerEvents: 'none'
      }}
    >
      <CopilotMenu activeCell={activeCell} />
    </div>
  );
};

const CopilotMenu: React.FC<any> = ({
  activeCell
}: {
  activeCell: Cell;
}): JSX.Element => {
  const [showRootMenu, setShowRootMenu] = useState(true);
  const [showCodeGenerator, setShowCodeGenerator] = useState(false);
  const [showCodeExplainer, setShowCodeExplainer] = useState(false);

  const onGenerateCodeClick = useCallback(() => {
    track('generateCodeSelected');
    setShowRootMenu(false);
    setShowCodeGenerator(true);
  }, [setShowRootMenu, setShowCodeGenerator]);

  const onExplainCodeClick = useCallback(() => {
    track('explainCodeSelected');
    setShowRootMenu(false);
    setShowCodeExplainer(true);
  }, [setShowRootMenu, setShowCodeExplainer]);

  // calculate MenuContainer position
  const { right, top } = useMemo(() => {
    const rect = activeCell.node.getBoundingClientRect();
    return {
      right: window.innerWidth - rect.width - rect.left + 187,
      top: rect.top
    };
  }, [activeCell]);

  const sdk = useCogniteSDK();
  if (!sdk) {
    return <div></div>;
  }

  return (
    <Copilot showChatButton={false} sdk={sdk}>
      <div
        id="copilot_menu_root"
        style={{
          height: '100vh',
          width: '100vw',
          pointerEvents: 'none'
        }}
      >
        {showRootMenu && (
          <MenuContainer id="copilot_main_menu" $top={top} $right={right}>
            <Menu>
              <Menu.Header>Cognite AI</Menu.Header>
              <Menu.Item
                icon="Code"
                iconPlacement="left"
                onClick={onGenerateCodeClick} // TODO: figure out why tf onMouseUp doesn't work
              >
                Generate code
              </Menu.Item>
              <Menu.Item icon="Edit" iconPlacement="left" disabled>
                Edit code
              </Menu.Item>
              <Menu.Item
                icon="LightBulb"
                iconPlacement="left"
                onClick={onExplainCodeClick}
              >
                Explain code
              </Menu.Item>
              <Menu.Item icon="Bug" iconPlacement="left" disabled>
                Fix code errors
              </Menu.Item>
            </Menu>
          </MenuContainer>
        )}
        {showCodeGenerator && (
          <MenuContainer id="copilot_generator_menu" $top={top} $right={right}>
            <CodeGeneratorInputPanel
              activeCell={activeCell}
              onClose={() => setShowCodeGenerator(false)}
            />
          </MenuContainer>
        )}
        {showCodeExplainer && (
          <MenuContainer id="copilot_explainer_menu" $top={top} $right={right}>
            <CodeExplainerPanel
              activeCell={activeCell}
              onClose={() => setShowCodeExplainer(false)}
            />
          </MenuContainer>
        )}
      </div>
    </Copilot>
  );
};

const MenuContainer = styled.div<{ $top: number; $right: number }>`
  position: absolute;
  top: ${props => props.$top}px;
  right: ${props => props.$right}px;
  padding-top: 36px;
  pointer-events: auto;
`;
