#include <boost/beast/core.hpp>
#include <boost/beast/http.hpp>
#include <boost/asio/dispatch.hpp>
#include <boost/asio/strand.hpp>
#include <boost/filesystem.hpp>
#include <algorithm>
#include <cstdlib>
#include <functional>
#include <iostream>
#include <memory>
#include <string>
#include <thread>
#include <vector>

namespace beast = boost::beast;         // from <boost/beast.hpp>
namespace http = beast::http;           // from <boost/beast/http.hpp>
namespace net = boost::asio;            // from <boost/asio.hpp>
using tcp = boost::asio::ip::tcp;               // from <boost/asio/ip/tcp.hpp>
namespace fs = boost::filesystem;

class http_server : public std::enable_shared_from_this<http_server> 
{
    net::io_context& ioc_;
    tcp::acceptor acceptor_;
    tcp::socket socket_{ioc_};
    beast::flat_buffer buffer_;
    http::request<http::string_body> req_;
    std::shared_ptr<std::string const> doc_root_;
public:
    http_server(net::io_context& ioc, tcp::endpoint endpoint) : 
        ioc_(ioc), acceptor_(ioc), socket_(ioc)
    {
        beast::error_code ec;
        
        // Open the acceptor
        acceptor_.open(endpoint.protocol(), ec);
        if (ec) {
            fail(ec, "open");
            return;
        }
        
        // Allow address reuse
        acceptor_.set_option(net::socket_base::reuse_address(true), ec);
        if(ec) {
            fail(ec, "set_option");
            return;
        }
        
        // Bind to the server address
        acceptor_.bind(endpoint, ec);
        if(ec) {
            fail(ec, "bind");
            return;
        }
        
        // Start listening for connections
        acceptor_.listen(net::socket_base::max_listen_connections, ec);
        if(ec) {
            fail(ec, "listen");
            return;
        }
    }
    
    void run() 
    {
        do_accept();
    }

private:
    void do_accept() 
    {
        acceptor_.async_accept(socket_, std::bind(&http_server::on_accept, 
shared_from_this(),std::placeholders::_1));
    }
    
    void on_accept(beast::error_code ec) 
    {
        if (ec) {
            fail(ec, "accept");
        } else {
            // Read a request
            do_read();
        }
    }
    
    void do_read() 
    {
        req_ = {};
        
        http::async_read(socket_, buffer_, req_, std::bind(&http_server::on_read, shared_from_this(), 
std::placeholders::_1, std::placeholders::_2));
    }
    
    void on_read(beast::error_code ec, std::size_t bytes_transferred) 
    {
        boost::ignore_unused(bytes_transferred);
        
        if (ec == http::error::end_of_stream) return do_close();
        if (ec) return fail(ec, "read");
        
        // Send the response
        handle_request(*doc_root_, std::move(req_), [this](auto&& res) {
            // The lifetime of the message has to extend for the duration of the async operation so we use a 
shared pointer to manage it.
            using response_type = typename std::decay<decltype(res)>::type;
            auto sp = std::make_shared<response_type>(std::forward<decltype(res)>(res));
            
            // Write the response
            http::async_write(socket_, *sp, [self = shared_from_this(), sp](beast::error_code ec, std::size_t 
bytes_transferred) {
                boost::ignore_unused(bytes_transferred);
                
                if (ec) return fail(ec, "write");
                
                // Clear contents of the request message, otherwise the read behavior is undefined.
                self->req_ = {};
                
                // If we should close the connection, do it by returning as no more operations will be allowed.
                if (sp->need_eof()) return do_close();
                
                // Read another request
                self->do_read();
            });
        });
    }
    
    void do_close() 
    {
        beast::error_code ec;
        socket_.shutdown(tcp::socket::shutdown_send, ec);
        
        // At this point the connection is closed gracefully
    }
};

int main(int argc, char* argv[]) 
{
    try {
        if (argc != 4) {
            std::cerr << "Usage: http-server-sync <address> <port> <doc_root>\n" << "Example:\n" << "http-server-sync 0.0.0.0 80 .\n";
            return EXIT_FAILURE;
        }
        
        auto const address = net::ip::make_address(argv[1]);
        auto const port = static_cast<unsigned short>(std::atoi(argv[2]));
        std::string doc_root{argv[3]};
        
        // The io_context is required for all I/O
        net::io_context ioc{1};
        
        // Create and launch a listening port
        std::make_shared<http_server>(ioc, tcp::endpoint{address, port})->run();
        
        // Run the I/O service on the requested number of threads
        std::vector<std::thread> v;
        v.reserve(1);
        for (auto i = v.size(); i > 0; --i) 
            v.emplace_back([&ioc] { ioc.run(); });
        
        ioc.run();
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }
}
