import React, { useState, useCallback, useEffect, useMemo } from 'react';
import { Cell } from '@jupyterlab/cells';
import { CodeGenerateFlow, useCopilotContext } from '@cognite/copilot-core';
import { Button, Flex, InputExp } from '@cognite/cogs.js';
import useCogniteSDK from '../lib/hooks/useCogniteSDK';
import { track } from '../lib/track';
import { secondsSince } from '../lib/helpers';
import { StyledContainer, StyledIcon } from './styled-components';
import { LoadingAnimation } from './LoadingAnimation';

export const CodeGeneratorInputPanel = ({
  activeCell,
  onClose
}: {
  activeCell: Cell;
  onClose: () => void;
}) => {
  const [inputValue, setInputValue] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const handleChange = useCallback(
    (e: any) => {
      setInputValue(e.target.value);
    },
    [setInputValue]
  );

  const sdk: any = useCogniteSDK();

  const { registerFlow, runFlow } = useCopilotContext();
  const generateFlow = useMemo(
    () => sdk && new CodeGenerateFlow({ sdk }),
    [sdk]
  );

  useEffect(() => {
    if (generateFlow) {
      const unregisterGenerate = registerFlow({ flow: generateFlow });
      return unregisterGenerate;
    }
  }, [generateFlow, registerFlow]);

  const handleSubmit = useCallback(
    (e: React.FormEvent) => {
      e.preventDefault();

      const startTime = Date.now();
      const prompt = inputValue;
      track('generateCodeRequested', { prompt });
      setIsGenerating(true);

      runFlow(generateFlow, {
        prompt
      }).then((response: any) => {
        track('codeGenerated', {
          prompt,
          response,
          responseSeconds: secondsSince(startTime)
        });
        (activeCell.model as any).value.text = response.content;
        onClose();
      });
    },
    [runFlow, inputValue]
  );

  const handleCancel = useCallback(() => {
    track('generateCodeCancelled', { inputValue });
    onClose();
  }, [inputValue, onClose]);

  return (
    <StyledContainer>
      <Flex direction="column">
        <Flex direction="row" justifyContent="space-between">
          <StyledIcon type="Code" size={36} />
          <div style={{ flexGrow: 1, marginLeft: 8 }}>
            <form onSubmit={handleSubmit}>
              <InputExp
                autoFocus
                clearable
                onChange={handleChange}
                size="large"
                fullWidth
                placeholder="Write a prompt to generate code"
                value={inputValue}
              />
            </form>
          </div>
        </Flex>
        <Flex
          direction="row"
          style={{ marginTop: 16 }}
          justifyContent="space-between"
        >
          <Button
            type="secondary"
            size="large"
            style={{ width: 136 }}
            onClick={handleCancel}
          >
            Cancel
          </Button>
          <Button
            type="primary"
            size="large"
            style={{
              color: '#fff',
              background: !inputValue || isGenerating ? '#b79df1' : '#6F3BE4',
              width: 136
            }}
            disabled={!inputValue || isGenerating}
            onClick={handleSubmit}
          >
            {isGenerating ? (
              <>
                <span>Generating</span>
                <LoadingAnimation style={{ height: 16, marginLeft: 8 }} />
              </>
            ) : (
              'Generate'
            )}
          </Button>
        </Flex>
      </Flex>
    </StyledContainer>
  );
};
