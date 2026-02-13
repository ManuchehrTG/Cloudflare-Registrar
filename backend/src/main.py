import asyncio
import uuid
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

# from src.api.exceptions.handlers import base_app_error_handler, generic_exception_handler, http_exception_handler
from src.api.router import api_router
from src.core.config import settings
# from src.shared.exceptions import BaseAppError
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
	try:
		yield
	except Exception as e:
		logger.error(f"⚠️ Startup failed: {e}", exc_info=True)
		raise
	finally:
		logger.info("🔴 Shutting down...")
		try:
			pass
		except Exception as e:
			logger.error(f"Error during shutdown: {e}", exc_info=True)


	# app.include_router(auth.router)
	# app.include_router(user.router)
	# app.include_router(theme.router)
	# app.include_router(message.router)

async def main() -> None:
	app = FastAPI(
		title=settings.app.title,
		version="1.0.0",
		lifespan=lifespan,
		docs_url="/api/docs" if settings.app.debug else None,
		swagger_ui_parameters={
			"persistAuthorization": True,
			# "operationsSorter": "method",
		}
	)

	@app.middleware("http")
	async def trace_id_middleware(request: Request, call_next):
		request.state.trace_id = str(uuid.uuid4())
		response = await call_next(request)
		response.headers["X-Trace-Id"] = request.state.trace_id
		return response

	# app.add_exception_handler(BaseAppError, base_app_error_handler)
	# app.add_exception_handler(HTTPException, http_exception_handler)
	# app.add_exception_handler(Exception, generic_exception_handler)
	# setup_exception_handlers(app)

	app.add_middleware(
		CORSMiddleware,
		allow_origins=settings.app.allowed_origins,
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
		# expose_headers=["New-Access-Token"]
	)

	app.include_router(api_router)

	config = uvicorn.Config(app=app, host=settings.app.host, port=settings.app.port, log_level="info")
	server = uvicorn.Server(config)

	await server.serve()

if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		logger.info("🔴 Server stopped gracefully")
