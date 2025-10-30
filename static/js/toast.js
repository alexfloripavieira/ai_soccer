/**
 * Toast Notification System
 *
 * Sistema de notificações toast para o AI Soccer.
 * Suporta 4 tipos: success, error, warning, info
 * Auto-dismiss configurável com barra de progresso
 * Suporte para múltiplos toasts empilhados
 * Animações suaves de entrada e saída
 */

class ToastManager {
  constructor() {
    this.container = null;
    this.template = null;
    this.toasts = [];
    this.defaultDuration = 5000; // 5 segundos
    this.maxToasts = 5; // Máximo de toasts simultâneos

    this.init();
  }

  /**
   * Inicializa o toast manager
   */
  init() {
    // Aguarda o DOM estar pronto
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.setup());
    } else {
      this.setup();
    }
  }

  /**
   * Configura os elementos do DOM
   */
  setup() {
    this.container = document.getElementById('toast-container');
    this.template = document.getElementById('toast-template');

    if (!this.container || !this.template) {
      console.warn('Toast container or template not found in DOM');
      return;
    }

    // Processa Django messages se existirem
    this.processDjangoMessages();
  }

  /**
   * Configurações de estilo por tipo de toast
   */
  getToastConfig(type) {
    const configs = {
      success: {
        borderColor: 'border-green-500',
        iconColor: 'text-green-400',
        progressColor: 'text-green-500',
        icon: 'M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z'
      },
      error: {
        borderColor: 'border-red-500',
        iconColor: 'text-red-400',
        progressColor: 'text-red-500',
        icon: 'M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z'
      },
      warning: {
        borderColor: 'border-yellow-500',
        iconColor: 'text-yellow-400',
        progressColor: 'text-yellow-500',
        icon: 'M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z'
      },
      info: {
        borderColor: 'border-blue-500',
        iconColor: 'text-blue-400',
        progressColor: 'text-blue-500',
        icon: 'M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z'
      }
    };

    return configs[type] || configs.info;
  }

  /**
   * Mostra um toast
   * @param {string} message - Mensagem a ser exibida
   * @param {string} type - Tipo do toast (success, error, warning, info)
   * @param {number} duration - Duração em ms (0 = não fecha automaticamente)
   */
  show(message, type = 'info', duration = null) {
    if (!this.container || !this.template) {
      console.warn('Toast system not initialized');
      return;
    }

    // Remove toasts excedentes se atingir o limite
    if (this.toasts.length >= this.maxToasts) {
      this.dismiss(this.toasts[0].id);
    }

    // Clona o template
    const toastElement = this.template.content.cloneNode(true).querySelector('.toast');
    const config = this.getToastConfig(type);

    // Gera ID único
    const toastId = `toast-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    toastElement.setAttribute('data-toast-id', toastId);

    // Aplica estilos
    toastElement.classList.add(config.borderColor);

    const icon = toastElement.querySelector('.toast-icon');
    icon.classList.add(config.iconColor);

    const iconPath = toastElement.querySelector('.toast-icon-path');
    iconPath.setAttribute('d', config.icon);
    iconPath.setAttribute('fill-rule', 'evenodd');
    iconPath.setAttribute('clip-rule', 'evenodd');

    // Define a mensagem
    const messageElement = toastElement.querySelector('.toast-message');
    messageElement.textContent = message;

    // Configura barra de progresso
    const progressBar = toastElement.querySelector('.toast-progress');
    progressBar.classList.add(config.progressColor);

    // Adiciona ao container
    this.container.appendChild(toastElement);

    // Anima entrada
    requestAnimationFrame(() => {
      toastElement.classList.remove('opacity-0', 'translate-x-full');
      toastElement.classList.add('opacity-100', 'translate-x-0');
    });

    // Configura botão de fechar
    const closeButton = toastElement.querySelector('.toast-close');
    closeButton.addEventListener('click', () => this.dismiss(toastId));

    // Configura auto-dismiss
    const dismissDuration = duration !== null ? duration : this.defaultDuration;
    let progressInterval = null;
    let timeoutId = null;

    if (dismissDuration > 0) {
      const startTime = Date.now();

      // Anima barra de progresso
      progressInterval = setInterval(() => {
        const elapsed = Date.now() - startTime;
        const remaining = Math.max(0, 100 - (elapsed / dismissDuration * 100));
        progressBar.style.width = `${remaining}%`;
      }, 50);

      // Auto-dismiss
      timeoutId = setTimeout(() => {
        this.dismiss(toastId);
      }, dismissDuration);
    } else {
      // Remove barra de progresso se não houver auto-dismiss
      progressBar.remove();
    }

    // Armazena referência
    this.toasts.push({
      id: toastId,
      element: toastElement,
      timeoutId,
      progressInterval
    });
  }

  /**
   * Remove um toast
   * @param {string} toastId - ID do toast a ser removido
   */
  dismiss(toastId) {
    const toastIndex = this.toasts.findIndex(t => t.id === toastId);
    if (toastIndex === -1) return;

    const toast = this.toasts[toastIndex];

    // Limpa timers
    if (toast.timeoutId) clearTimeout(toast.timeoutId);
    if (toast.progressInterval) clearInterval(toast.progressInterval);

    // Anima saída
    toast.element.classList.remove('opacity-100', 'translate-x-0');
    toast.element.classList.add('opacity-0', 'translate-x-full');

    // Remove do DOM após animação
    setTimeout(() => {
      if (toast.element.parentNode) {
        toast.element.parentNode.removeChild(toast.element);
      }
    }, 300);

    // Remove da lista
    this.toasts.splice(toastIndex, 1);
  }

  /**
   * Remove todos os toasts
   */
  dismissAll() {
    [...this.toasts].forEach(toast => this.dismiss(toast.id));
  }

  /**
   * Processa Django messages e exibe como toasts
   */
  processDjangoMessages() {
    const messagesContainer = document.getElementById('django-messages');
    if (!messagesContainer) return;

    const messages = messagesContainer.querySelectorAll('.django-message');
    messages.forEach(messageEl => {
      const message = messageEl.textContent.trim();
      const type = messageEl.getAttribute('data-type') || 'info';

      // Mapeia tipos do Django para tipos de toast
      const typeMap = {
        'success': 'success',
        'error': 'error',
        'warning': 'warning',
        'info': 'info',
        'debug': 'info'
      };

      this.show(message, typeMap[type] || 'info');
    });

    // Remove o container de mensagens Django após processar
    messagesContainer.remove();
  }

  /**
   * Atalhos para tipos específicos
   */
  success(message, duration = null) {
    this.show(message, 'success', duration);
  }

  error(message, duration = null) {
    this.show(message, 'error', duration);
  }

  warning(message, duration = null) {
    this.show(message, 'warning', duration);
  }

  info(message, duration = null) {
    this.show(message, 'info', duration);
  }
}

// Inicializa e expõe globalmente
const toast = new ToastManager();

// Expõe no objeto window para uso global
window.toast = toast;

// Também expõe métodos individuais para conveniência
window.showToast = (message, type, duration) => toast.show(message, type, duration);
window.toastSuccess = (message, duration) => toast.success(message, duration);
window.toastError = (message, duration) => toast.error(message, duration);
window.toastWarning = (message, duration) => toast.warning(message, duration);
window.toastInfo = (message, duration) => toast.info(message, duration);
