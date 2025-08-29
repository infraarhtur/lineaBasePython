from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# Instancia del esquema de seguridad HTTPBearer
security = HTTPBearer(auto_error=False)

def get_bearer_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> str:
    """
    Dependencia de FastAPI que valida que se proporcione un Bearer token.
    Esta función se puede usar como dependencia en los endpoints.
    
    Args:
        credentials (HTTPAuthorizationCredentials): Credenciales extraídas automáticamente por FastAPI
        
    Returns:
        str: El token extraído y validado
        
    Raises:
        HTTPException: Si no se proporciona el token o el formato es incorrecto
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autorización requerido"
        )
    
    token = credentials.credentials
    
    if not token or not token.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no puede estar vacío"
        )
    
    return token

def verify_bearer_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> str:
    """
    Función wrapper que utiliza HTTPBearer para validar el token.
    Esta función se puede usar como dependencia en los endpoints.
    
    Args:
        credentials (HTTPAuthorizationCredentials): Credenciales extraídas automáticamente por FastAPI
        
    Returns:
        str: El token validado
        
    Raises:
        HTTPException: Si no se proporciona el token o el formato es incorrecto
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autorización requerido"
        )
    
    token = credentials.credentials
    
    if not token or not token.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no puede estar vacío"
        )
    
    return token
