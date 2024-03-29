'use client';

import { useEffect } from 'react';
import Router from 'next/router';
import Cookies from 'js-cookie';

const useAuth = () => {
  useEffect(() => {
    const Token = Cookies.get('Token');

    if (!Token) {
      window.location.href = '/auth/login';
    }
  }, []);
};

export default useAuth;
